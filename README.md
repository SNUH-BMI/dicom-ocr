# dicom-ocr
Extract text from DEXA report using AWS Textract

# Notes

<li>The requirements.txt file should be installed first using:</li>
<code>pip install -r requirements.txt</code>
</br></br>
<li>Make sure that you set up the AWS SDK.</li>
You have to set credentials in the AWS credentials profile file on you local system.
Reference: <link>https://docs.aws.amazon.com/textract/latest/dg/setup-awscli-sdk.html</link>
</br></br>
<li>Change Working Directory</li>
For example:
if you downloaded the files in path 'C:/Users/my/folder'</br>
change
<code>%run C:/Users/mchoi/Desktop/dicom/read_dicom.py --path ~</code></br>
to
<code>%run C:/Users/my/folder/read_dicom.py --path ~</code>
