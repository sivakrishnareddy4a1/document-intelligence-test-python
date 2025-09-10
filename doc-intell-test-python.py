# !pip install azure-identity azure-storage-blob azure-ai-documentintelligence
# !pip install azure-ai-formrecognizer

# import sys
# !{sys.executable} -m pip install azure-identity azure-storage-blob azure-ai-documentintelligence

# import sys
# !{sys.executable} -m pip install azure-identity azure-storage-blob azure-ai-documentintelligence --upgrade


import os
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
#from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.storage.blob import BlobClient

# ---- Configuration ----
storage_account_url = "https://testdocntelligence.blob.core.windows.net/"
container_name = "test"
blob_name = "blank header.png"

form_recognizer_endpoint = "https://acctest-cogacc-230630032807723157.cognitiveservices.azure.com/"
model_id = "prebuilt-invoice"   # or custom model id

# ---- Auth with Azure AD ----
credential = DefaultAzureCredential()

# ---- Get file from Blob ----
blob_client = BlobClient(
    account_url=storage_account_url,
    container_name=container_name,
    blob_name=blob_name,
    credential=credential
)

download_stream = blob_client.download_blob()
file_data = download_stream.readall()

# ---- Send file to Document Intelligence ----
document_client = DocumentIntelligenceClient(
    endpoint=form_recognizer_endpoint,
    credential=credential
)

poller = document_client.begin_analyze_document(
    model_id=model_id,
    body=file_data
)

result = poller.result()

# ---- Print extracted content ----
for idx, page in enumerate(result.pages):
    print(f"\nPage {idx+1}")
    for line in page.lines:
        print(line.content)