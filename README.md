# AWS SQS & Lambda — Resiliência na Integração ERP SAP

Este projeto implementa um padrão de arquitetura resiliente baseada em eventos (*Event-Driven Architecture*) utilizando recursos serverless da **AWS (SQS + Lambda em Python)** para garantir o processamento confiável de ordens de venda originadas de e-commerce com destino ao **SAP ERP**.

---

## 📐 Arquitetura da Solução

```text
[E-commerce / Webhook] 
       │
       ▼ (Envio do Pedido)
[SQS: sap-orders-queue] ◄──── (Tentativas / Retry)
       │                                │
       ▼ (Disparo Automático)           │ (Erro de API)
[Lambda: sap-integration-lambda-retry] ─┘
       │
       ▼ (Após 3 falhas seguidas)
[SQS: sap-orders-dlq] (Isolamento de Segurança)

Fluxo de Processamento:
Webhook / Ingestão: Um simulador em Python envia requisições JSON estruturadas no padrão de APIs do SAP (DocEntry, CardCode, etc.) para a fila principal do SQS.

Desacoplamento: O Amazon SQS (sap-orders-queue) retém as mensagens e atua como buffer, protegendo o ERP contra picos de acesso.

Processamento Serverless: A função AWS Lambda (sap-integration-lambda-retry) é disparada automaticamente por evento para processar os lotes.

Resiliência e Retry: Caso ocorra uma falha de comunicação ou timeout na API do SAP, a Lambda lança uma exceção. O SQS gerencia as tentativas com política de retentativa configurada (maxReceiveCount = 3).

Isolamento de Falhas (DLQ): Se a mensagem falhar após 3 tentativas, o SQS a direciona para a Dead-Letter Queue (sap-orders-dlq), evitando o travamento da fila principal (Head-of-Line Blocking).

DLQ Redrive: Suporte a reprocessamento manual ou automatizado das mensagens da DLQ após a recuperação dos serviços do SAP.

🛠️ Tecnologias Utilizadas
AWS SQS: Filas padrão e Dead-Letter Queue (DLQ).

AWS Lambda: Runtime Python 3.12 com suporte a gatilhos orientados a eventos.

AWS IAM: Gerenciamento de políticas com privilégio mínimo (AWSLambdaSQSQueueExecutionRole).

Amazon CloudWatch: Monitoramento centralizado e auditoria de logs.

Boto3 (Python SDK): Envio programático de dados simulando webhook corporativo.

🚀 Como Reproduzir este Projeto
Pré-requisitos
Conta na AWS com permissões para SQS, Lambda e IAM.

Python 3.10+ e biblioteca boto3 instalada.

Passos de Implantação
Criar as Filas SQS:

Crie a DLQ sap-orders-dlq (Fila padrão).

Crie a fila principal sap-orders-queue e associe a DLQ na seção Fila de mensagens mortas com maxReceiveCount = 3.

Criar a Função Lambda:

Crie a função sap-integration-lambda-retry utilizando o runtime Python 3.12.

Adicione o código do arquivo src/lambda_function.py.

Na aba de Permissões (IAM), anexe a política AWSLambdaSQSQueueExecutionRole.

Configurar o Trigger:

Adicione a fila sap-orders-queue como gatilho (Trigger) na função Lambda.

Executar a Simulação:

Execute o script src/simulador_webhook.py para gerar eventos de teste.

🛡️ Governança e Segurança
Tags aplicadas: Project: SAP-Integration-Resilience

Políticas de Acesso: Princípio do menor privilégio aplicado à Role de execução da Lambda.

Chaves de Acesso: Credenciais temporárias geradas exclusivamente para o teste local e desativadas após validação.
