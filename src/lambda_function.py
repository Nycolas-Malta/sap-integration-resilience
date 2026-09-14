import json
import logging

# Configuração de logs para monitoramento via CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Recebido lote de {len(event['Records'])} mensagem(ns) do SQS.")
    
    for record in event['Records']:
        message_id = record['messageId']
        payload = json.loads(record['body'])
        
        doc_entry = payload.get('DocEntry', 'N/A')
        card_code = payload.get('CardCode', 'N/A')
        simular_erro = payload.get('SimularErro', False)
        
        logger.info(f"[PROCESSANDO] Pedido SAP Entry: {doc_entry} | Cliente: {card_code}")
        
        # Simulação de regra de negócio / comunicação com API SAP
        if simular_erro:
            logger.error(f"[FALHA INTEGRACAO SAP] Timeout/Erro na API SAP para o Pedido {doc_entry}. Forçando exceção para disparo do SQS Retry.")
            raise Exception(f"Erro de comunicação com endpoint do SAP para o Pedido {doc_entry}")
        
        logger.info(f"[SUCESSO INTEGRACAO SAP] Pedido {doc_entry} gravado no ERP SAP com sucesso!")

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído com sucesso!')
    }
