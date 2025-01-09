#!/bin/bash

# Variáveis para o domínio e as configurações do backend
backend_hostname="seudominio.com.br"
backend_port="5000"  # Altere para a porta correta do seu backend
email_cert="seu@email.com" # Email para o certificado

# Criação do arquivo de configuração do Nginx para o domínio
cat > /etc/nginx/sites-available/${backend_hostname} << EOF
server {
  server_name ${backend_hostname};
  location / {
    proxy_pass http://127.0.0.1:${backend_port};
    proxy_http_version 1.1;
    proxy_set_header Upgrade \$http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_cache_bypass \$http_upgrade;
  }
}
EOF

# Ativação do site
ln -s /etc/nginx/sites-available/${backend_hostname} /etc/nginx/sites-enabled/

# Verificação e reinício do Nginx
nginx -t && systemctl restart nginx

# Adicionando o SSL com Certbot
certbot -m $email_cert \
        --nginx \
        --agree-tos \
        --non-interactive \
        --domains $backend_hostname

echo "Configuração do Nginx para ${backend_hostname} concluída."