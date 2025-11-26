#!/bin/bash
gcloud run deploy cube-credit-card-mcp \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars UCL8C032_API_ENDPOINT=https://ucl8c032-mock-api-915548793631.asia-east1.run.app/UCL8C032,CCPBNTCAP04Q001_API_ENDPOINT=https://ccp-b-ntcap04q001-mock-api-915548793631.asia-east1.run.app/CCP-B-NTCAP04Q001,CCPCNTUSE27CUBEQC01_API_ENDPOINT=https://ccp-c-ntuse27cubeqc01-mock-api-915548793631.asia-east1.run.app/CCP-C-NTUSE27CUBEQC01
