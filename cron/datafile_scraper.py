import os
import requests
import ddddocr

from logging import Logger
from settings import settings

class DataFileScraper:
    
    def __init__(self, logger:Logger) -> None:
        self._req_session = requests.Session()
        self._file_download_dir = settings.DOWNLOAD_DIR
        self._base_url = settings.BASE_URL
        self._resource_url = settings.RESOURCE_PAGE
        self._resource_origin = settings.RESOURCE_ORIGIN
        self._resource_id = settings.RESOURCE_ID
        self.logger = logger
        self._add_req_headers()
        
        
    def _add_req_headers(self) -> None:
        
        HEADERS = {
                    "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/148.0.0.0 Safari/537.36"
                    ),
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "Origin": self._resource_origin,
                    "Referer": self._resource_url,
                }
        
        self._req_session.headers.update(HEADERS)
    
    def _download_captcha_image(self) -> str:
        
        self.logger.info("[CSV FILE DOWNLOAD] Captca image download started...")

        if not os.path.exists(self._file_download_dir):
            os.makedirs(self._file_download_dir, exist_ok=True)
            
        file_path = f"{self._file_download_dir}/captcha.png"
        
        res = self._req_session.get(settings.BASE_URL)        
        res.raise_for_status()
        
        data  = res.json()
        
        self.captcha_sid = data["sid"]
        self.captcha_token = data["token"]
        
        image_base_url = self._base_url.split("v1/")[0] 
        image_url = f"{image_base_url}v1{data["url"]}"
        
        res = self._req_session.get(image_url)
        
        self.logger.info("[CSV FILE DOWNLOAD] Download successfull...")
        with open(file_path, mode="wb") as f:
            f.write(res.content)
        
        return file_path
    
    
    def _ocr_captcha_image(self, image_path:str) -> str:
        ocr = ddddocr.DdddOcr()
        self.logger.info("[CSV FILE DOWNLOAD] Captcha ocr started...")
        with open(image_path, "rb") as f:
            img = f.read()

        result = ocr.classification(img)
        
        if not result:
            raise Exception("Error solving image captcha")

        self.logger.info("[CSV FILE DOWNLOAD] Captcha solved successfully...")
        os.remove(image_path)
        return str(result).upper()
    
    
    def _send_payload(self, captcha_text:str) -> str:
        
        self.logger.info("[CSV FILE DOWNLOAD] Sending post payload...")
        
        payload = {
            "name": [{"value": "Resource Download"}],
            "field_domain": ["4"],
            "field_domain_visibility": ["4", "4"],
            "catalog_id": [{"target_id": ""}],
            "export_status": [{"value": "download"}],
            "file_type": [{"value": "csv"}],
            "ip": [{"value": ""}],
            "ogdp_captcha_response": [{"value": captcha_text}],
            "ogdp_captcha_sid": [{"value": self.captcha_sid}],
            "ogdp_captcha_token": [{"value": self.captcha_token}],
            "parameters": {},
            "purpose": [{"value": "3"}],
            "resource_id": [{"target_id": self._resource_id}],
            "uid": [{"value": 0}],
            "usage": [{"value": "2"}]
        }
        
        request_url = self._base_url.replace("captcha/refresh/image/", '')
        res = self._req_session.post(request_url, json=payload)
        res.raise_for_status()
        data  = res.json()
        self.logger.info("[CSV FILE DOWNLOAD] Request successfull...")
        return data["download_url"]

    def _pincode_csv_downloader(self, download_url:str) -> str:
        self.logger.info("[CSV FILE DOWNLOAD] Downloadind csv file started...")
        
        file_name = f"{self._file_download_dir}/datafile.csv"
        
        file_contents = self._req_session.get(download_url)
        
        with open(file_name, "wb") as f:
            for chunk in file_contents.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
        
        self.logger.info("[CSV FILE DOWNLOAD] Download complete...")
        return file_name
    
    def start(self) -> str:
        
        image_path = self._download_captcha_image()
        captcha_text = self._ocr_captcha_image(image_path)
        download_url = self._send_payload(captcha_text)
        filename = self._pincode_csv_downloader(download_url)
        return filename