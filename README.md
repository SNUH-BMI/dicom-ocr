# dicom-ocr
Extract text from DEXA report using AWS Textract

## Before you run code

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

## How it works
<dl>
  <dt>Phase 1 - Read DICOM files</dt>
  <dd>다이콤파일에는 dataset이라는게 존재합니다.<br>
    이 단계에서는 모든 다이콤파일의 특정 dataset들을 읽어서 csv파일로 저장합니다.
  </dd>
  <dt>Phase 2 - Convert dcm to png</dt>
  <dd>다이콤파일의 dataset을 읽다보면 'Pixel Data'라는 값이 있습니다.<br>
    이 안에 우리가 필요한 검사결과 이미지의 픽셀값이 담겨있습니다.<br>
    이 값을 이용해서 검사결과 이미지를 png로 생성해 줍니다.<br>
    ProtocolName(사진촬영부위, spine, left femur, right femur 등)별로 폴더가 생성됩니다.
  </dd>
  <dt>Phase 3 - Extract text from image using AWS Textract</dt>
  <dd>이제부터는 Phase 2에서 생성된 폴더별로 코드가 동작하게 됩니다.(코드에 디렉토리를 설정해주어야 합니다.)<br>
    Textract를 이용해서 이미지 파일 안의 모든 글자를 OCR 합니다.<br>
    특정 ProtocolName (예를 들면 AP Spine)폴더 안에 json 폴더가 생성되고(경로 예: 'AP Spine/json'), 이 안에 각 이미지 별 OCR한 내용이 JSON 파일로 저장됩니다.
  </dd>
  <dt>Phase 4 - Export tabular data into a csv file</dt>
  <dd> 이미지의 모든 텍스트가 필요한 것이 아니라, 표 안에 들어있는 검사수치만 필요하기 때문에 값들을 솎아줍니다.<br>
    코드 실행 전 json 폴더로 디렉토리 설정을 해주어야 합니다.(경로 예: 'AP Spine/json')
    같은 폴더 안에 output.csv 파일이 생성됩니다.<br>
    OCR한 결과가 100% 정확하지 않기 때문에 별도의 데이터 QC가 필수적입니다.<br>
    <img src=https://user-images.githubusercontent.com/42328721/101576590-a95ef500-3a1c-11eb-96e9-885ee5ecb963.png>
  </dd>
  <dt>Phase 5 - Reshape data based on column of the csv file</dt>
  <dd> QC된 데이터를 pandas 라이브러리를 이용하여 재구성합니다. <br>
    코드 실행 전 output.csv 파일의 경로를 설정해주어야 합니다.(경로 예: 'AP Spine/json/output.csv')
    Phase 4 이후 데이터 QC를 제대로 하지 않으면 코드가 동작하지 않을 수 있습니다.<br>
    <img src=https://user-images.githubusercontent.com/42328721/101577226-d7dcd000-3a1c-11eb-8397-5eaa0e072038.png>
  </dd>
</dl>

### What is drop_duplicates_from_records.ipynb for?
<dl>
  <dt>중복 레코드가 존재할 수 있습니다.</dt>
  <dd>cdm에 옮길 데이터에는 중복 레코드가 없어야 합니다. </br>
      중복 데이터를 거르는 기준은 환자번호와 검사일자 입니다.</br>
      데이터를 선택하는 자세한 방법은 파일을 확인해주세요.
  </dd>
  <dt>준비사항</dt>
  <dd><b>Phase1</b>에서 생성된 dataset csv파일을 <b>Phase5</b>의 csv 파일과 filename을 기준으로 join 합니다.</br>
      두 개의 csv 파일에서 filename의 패턴이 동일하지 않을 수 있으며, pandas 등의 라이브러리를 이용해 수정해주시면 됩니다. </br> 
      결과는 xlsx 파일로 생성하면 코드 수정없이 셀을 실행시킬 수 있습니다. (단, 200만 레코드 이상일 경우에는 csv 파일로 생성하거나, 연도별로 파일을 나누는 것을 추천합니다.) 
      이 때 촬영부위별(spine, left femur, right femur)로 sheet를 나눠줍니다.
  </dd>
</dl>
