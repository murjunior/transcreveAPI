# API de Transcrição de Áudio para Texto
Uma API simples criada com Python Flask e a biblioteca SpeechRecognition para transcrever arquivos de áudio em texto. A API possui um único endpoint em `/transcrever`, que pode ser usado para enviar arquivos de áudio para transcrição.

Por exemplo, usando o comando `curl` no terminal:

```
curl -X POST -F 'audio=@/path/to/audio.wav' http://localhost:5444/transcrever
```


## Instalação

### 1. Editar [main.py](https://github.com/murjunior/transcreveAPI/blob/master/main.py) e [tcr.sh](https://github.com/murjunior/transcreveAPI/blob/master/tcr.sh)

Em **main.py**
```js
CORS(app, origins="https://app.seu-frontend.com.br") //Endereço do seu frontend
```

Em **tcr.sh**
```js
backend_hostname="transcreve-api.seudominio.com.br" //Altere para o endereço que será sua API de transcrição
backend_port="5444"  //Altere para a porta correta do seu backend
email_cert="seu@email.com" //Email para o certificado
```

> [!IMPORTANT]
> Lembre-se de criar um endereço para sua api de transcrição no CloudFlare e apontar para o ip da sua VPS.

### 2. Depois de <ins>editado os arquivos</ins> do passo 1, envie para a pasta /root da sua VPS.

### 3. Acessa a pasta de onde você enviou os arquivos
```
cd /root/transcreveAPI
```

### 4. Realizar o Build da imagem do container em docker
```
docker build -t transcreve-api:1.1 .
```
> [!WARNING]
> Nesta etapa já estamos assumindo que você tenha o docker rodando em sua máquina.

### 5. Criar o container no docker com a imagem que acabou de criar
```
docker run -d -p 5444:5444 --name transcreve-api transcreve-api:1.1
```

### 6. Criar dominio no Nginx e solicitar SSL para o dominio da API

a. Entrar na pasta que subiu na VPS
```
cd /root/transcreveAPI
```
b. Dar permissão para execução do script.
```
chmod +x tcr.sh
```
c. Executar o script
```
./tcr.sh
```

### 7. Por fim só realizar a alteração no seu código para que ele envie o audio para a API e realize a transcrição.


## Contribuindo

Sinta-se à vontade para copiar ou contribuir com a API criando pull requests.
