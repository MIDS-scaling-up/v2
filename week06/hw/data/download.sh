# Install zip 
apt-get install unzip
# Download Bert pretrained - https://github.com/google-research/bert/blob/master/README.md
wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip
wget https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip
# Unzip files
unzip cased_L-12_H-768_A-12.zip
unzip uncased_L-12_H-768_A-12.zip 
# Download and unzip training and test files
wget https://s3-eu-west-1.amazonaws.com/darraghdog1/train.csv.zip
wget https://s3-eu-west-1.amazonaws.com/darraghdog1/test.csv.zip
unzip train.csv.zip
unzip test.csv.zip
# Remove all the zip files
rm *.zip
