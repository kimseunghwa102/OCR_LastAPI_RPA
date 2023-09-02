import os
import tempfile
import pandas as pd
import pdfplumber
import requests
import uuid
import time
import json

api_url = 'null'
secret_key = 'null'
directory_path = 'null'

image_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(('.png', '.pdf'))]

results = []

for image_file in image_files:
    ext = os.path.splitext(image_file)[1]
    request_json = {
        'images': [
            {
                'format': 'pdf' if ext == '.pdf' else 'png',
                'name': 'name'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}

    with open(image_file, 'rb') as f:
        files = [('file', f)]
        headers = {'X-OCR-SECRET': secret_key}
        response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

    response_data = json.loads(response.text)
    fields_data = response_data.get('images', [{}])[0].get('fields', [])
    fields_dict = {item['name']: {'text': item['inferText'], 'confidence': item['inferConfidence']} for item in fields_data}
    
    # 데이터 프레임 작성 로직은 그대로 유지
    keys =  ["작성자", "접수번호", "의뢰자", "형식", "기기번호", "교정일자", "온도최저", "온도최고", "습도최저", "습도최고", "기기명", "제작회사및형식", "기기번호SN", "차기교정예정일자", "교정기관", "기기명1", "제작회사및형식1", "기기번호SN1", "차기교정예정일자1", "교정기관1", "X축측정정확도","Y축측정정확도"]
    text_keys = [f"{key}_text" for key in keys]
    confidence_keys = [f"{key}_confidence" for key in keys]
    all_keys = []

    for text_key, conf_key in zip(text_keys, confidence_keys):
        all_keys.extend([text_key, conf_key])

    data = {}
    for key, text_key, conf_key in zip(keys, text_keys, confidence_keys):
        data[text_key] = [fields_dict.get(key, {}).get('text', "")]
        data[conf_key] = [fields_dict.get(key, {}).get('confidence', "")]

    df = pd.DataFrame(data, columns=all_keys)
    results.append(df)
    # ...

final_df = pd.concat(results, ignore_index=True)
excel_path = 'C:\\Users\\seukim\\Downloads\\result.xlsx'
final_df.to_excel(excel_path, index=False)

print(f"Results written to {excel_path}")
