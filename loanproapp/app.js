const sharp = require('sharp');
const Tesseract = require('tesseract.js');
const AWS = require('aws-sdk');
const fs = require('fs');

// Initialize AWS SDK
AWS.config.update({
    accessKeyId: 'AKIAXYNPLMJNG52VCO6B', // Your AWS Access Key ID
    secretAccessKey: 'QkO8WBDozAKOvpaLnzVH9yIuUxeH2xWHY4OGg1/V', // Your AWS Secret Access Key
    region: 'us-east-1'
});

// Initialize S3 client
const s3 = new AWS.S3();

// Bucket name and directory paths
const bucketName = 'loanprocessingapp';
const sourceDirectoryPath = 'documents/';
const destinationDirectoryPath = 'ProcessedDocuments/';
const tempDir = 'temp_images';

// Create temp directory if it doesn't exist
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir);
}

// Function to download images from S3
function downloadImagesFromS3() {
    const params = {
        Bucket: bucketName,
        Prefix: sourceDirectoryPath
    };

    s3.listObjectsV2(params, (err, data) => {
        if (err) {
            console.error('Error fetching S3 objects:', err);
            return;
        }

        data.Contents.forEach(obj => {
            const key = obj.Key;
            const filename = key.split('/').pop();
            const downloadPath = `${tempDir}/${filename}`;

            const fileStream = fs.createWriteStream(downloadPath);
            const params = {
                Bucket: bucketName,
                Key: key
            };

            s3.getObject(params)
                .createReadStream()
                .pipe(fileStream)
                .on('error', err => {
                    console.error(`Error downloading file ${filename}:`, err);
                })
                .on('close', () => {
                    console.log(`Downloaded file: ${filename}`);
                    processImage(downloadPath);
                });
        });
    });
}

// Function to preprocess images before OCR using Sharp
async function preprocessImage(imagePath) {
    try {
        const image = sharp(imagePath);
        const imageName = imagePath.split('/').pop();

        // Apply operations to enhance image quality and potentially remove weak lines
        const preprocessedImageBuffer = await image
            .resize({ width: 800 }) // Resize the image to a suitable width
            .greyscale() // Convert the image to greyscale
            .extract({ left: 260, top: 100, width: 500, height: 300 })
            .sharpen() // Sharpen the image to enhance edges
            .toBuffer(); // Convert the image to a Buffer

        // Save the preprocessed image
        const preprocessedImagePath = `${tempDir}/preprocessed_${imageName}`;
        fs.writeFileSync(preprocessedImagePath, preprocessedImageBuffer);

        return { imageName, preprocessedImagePath };
    } catch (error) {
        console.error('Error preprocessing image:', error);
        throw error;
    }
}

// Function to extract text from preprocessed images using Tesseract.js
function extractTextFromImage(preprocessedImagePath, imageName) {
    Tesseract.recognize(
        preprocessedImagePath,
        'eng',
        { logger: info => console.log(info) }
    ).then(({ data: { text } }) => {
        console.log(`Text extracted from ${preprocessedImagePath}:`);
        console.log(text);

        // Write the extracted text into a text file
        writeAndUploadTextFile(imageName, text.split('\n'));
    }).catch(error => {
        console.error(`Error processing image ${preprocessedImagePath}:`, error);
    });
}

// Function to write extracted text into a text file and upload to S3
function writeAndUploadTextFile(imageName, extractedData) {
    const textData = extractedData.join('\n');
    const textFilePath = `${tempDir}/${imageName}.txt`;

    fs.writeFile(textFilePath, textData, (err) => {
        if (err) {
            console.error('Error writing text file:', err);
        } else {
            console.log(`Text file saved: ${textFilePath}`);

            const fileStream = fs.createReadStream(textFilePath);
            const uploadParams = {
                Bucket: bucketName,
                Key: `${destinationDirectoryPath}${imageName}.txt`,
                Body: fileStream
            };

            s3.upload(uploadParams, (err, data) => {
                if (err) {
                    console.error('Error uploading file to S3:', err);
                } else {
                    console.log(`Uploaded file to S3: ${data.Location}`);
                }
            });
        }
    });
}

// Function to process images
function processImage(imagePath) {
    preprocessImage(imagePath)
        .then(({ imageName, preprocessedImagePath }) => {
            console.log('Image preprocessed:', preprocessedImagePath);

            // Extract text from preprocessed image
            extractTextFromImage(preprocessedImagePath, imageName);
        })
        .catch(error => {
            console.error('Error preprocessing image:', error);
        });
}

// Main function
function main() {
    downloadImagesFromS3();
}

// Run the main function
main();
