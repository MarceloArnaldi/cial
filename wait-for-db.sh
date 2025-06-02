#!/bin/sh

echo "Aguardando o banco de dados..."

until pg_isready -h db -p 5432 -U postgres; do
  sleep 10
done

echo "Banco de dados está pronto! Iniciando app..."
exec python app.py
