import json
import google_cloud.oauth as oauth, google_cloud.drive as gdrive, google_cloud.docs as gdocs
from pprint import pp

google_creds = oauth.GoogleOAuth('credentials.json').authenticate(oauth.GoogleOAuthScopes.DRIVE)
drive_api = gdrive.GoogleDriveApi(google_creds)
docs_api = gdocs.GoogleDocsApi(google_creds)

for template in json.load(open('templates.json')):
    requests = [gdocs.ReplaceAllTextRequest(placeholder, value)
        for placeholder,value in template['placeholders'].items()]
    for document_id in template['document_ids']:
        copy_id = drive_api.copy(document_id)
        docs_api.batch_update(copy_id, requests)
        file_content = drive_api.export_media(copy_id, gdrive.MimeType.PDF)
        drive_api.delete(copy_id)
        with open(f'{copy_id}.pdf', 'wb') as f:
            f.write(file_content)
