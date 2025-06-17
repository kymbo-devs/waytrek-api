import boto3
from botocore.exceptions import ClientError
import os
from config import settings
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_s3_client():
    try:
        logger.info("Inicializando cliente S3...")
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION
        )
        
        s3_client.list_buckets()
        logger.info("Cliente S3 inicializado correctamente")
        
        return s3_client
    except Exception as e:
        logger.error(f"Error al inicializar el cliente S3: {str(e)}")
        raise

def list_buckets():
    try:
        s3_client = get_s3_client()
        response = s3_client.list_buckets()
        
        print("\n=== S3 Buckets ===")
        for bucket in response['Buckets']:
            creation_date = bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")
            print(f"\nBucket Name: {bucket['Name']}")
            print(f"Creation Date: {creation_date}")
            
            try:
                location = s3_client.get_bucket_location(Bucket=bucket['Name'])
                region = location['LocationConstraint'] or 'us-east-1'
                print(f"Region: {region}")
            except ClientError:
                print("Region: Not available")
                
        print("\nTotal de buckets:", len(response['Buckets']))
        
    except ClientError as e:
        logger.error(f"Error listing buckets: {str(e)}")
        raise

def upload_file_to_s3(file_data, file_name, content_type=None):
    try:
        logger.info(f"Subiendo archivo {file_name} a S3...")
        s3_client = get_s3_client()
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
            
        s3_client.upload_fileobj(
            Fileobj=file_data,
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_name,
            ExtraArgs=extra_args
        )
        logger.info(f"Archivo {file_name} subido exitosamente")
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {str(e)}")
        raise

    # Generate the file URL
    url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/{file_name}"
    return url

def delete_file_from_s3(file_name):
    try:
        logger.info(f"Eliminando archivo {file_name} de S3...")
        s3_client = get_s3_client()
        s3_client.delete_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_name
        )
        logger.info(f"Archivo {file_name} eliminado exitosamente")
    except ClientError as e:
        logger.error(f"Error deleting file from S3: {str(e)}")
        raise 

def generate_presigned_url(file_key: str, expires_in: int = 600):
    try:
        logger.info(f"Generando pre-signed URL para {file_key}...")
        s3_client = get_s3_client()
        
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.S3_BUCKET_NAME, 'Key': file_key},
            ExpiresIn=expires_in
        )
        
        logger.info(f"Pre-signed URL generada exitosamente para {file_key}")
        return presigned_url
        
    except ClientError as e:
        logger.error(f"Error generating presigned URL: {str(e)}")
        raise 

