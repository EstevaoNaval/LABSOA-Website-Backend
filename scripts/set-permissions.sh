#!/bin/sh
# Define o grupo que terá acesso ao diretório. Usa "appdata" como padrão.
GROUP_NAME=${DATA_GROUP:-appdata}

# Define o caminho do diretório compartilhado
DATA_DIR=${DATA_ROOT_DIR}

# Se o grupo não existir, cria-o
if ! getent group "$GROUP_NAME" >/dev/null; then
    echo "Creating group $GROUP_NAME..."
    addgroup -g "$DATA_GID" "$GROUP_NAME"
fi

# Criar usuários e adicioná-los ao grupo comum
for USER_INFO in $USERS; do
    USER=$(echo "$USER_INFO" | cut -d':' -f1)
    USER_UID=$(echo "$USER_INFO" | cut -d':' -f2)

    if ! id "$USER" >/dev/null 2>&1; then
        echo "Criando usuário $USER com UID $USER_UID e adicionando ao grupo $GROUP_NAME..."
        adduser -D -u "$USER_UID" -G "$GROUP_NAME" "$USER"
    else
        echo "Usuário $USER já existe. Garantindo que ele esteja no grupo $GROUP_NAME..."
        adduser "$USER" "$GROUP_NAME"
    fi
done

# Ajusta a propriedade do diretório para que o grupo seja o definido
echo "Setting group '$GROUP_NAME' for $DATA_DIR..."
chown -R :"$GROUP_NAME" "$DATA_DIR"

# Ajusta as permissões recursivamente para 2775:
# - Dono: leitura, escrita, execução.
# - Grupo: leitura, escrita, execução.
# - Outros: leitura e execução.
chmod -R 2775 "$DATA_DIR"

# Aplica o bit setgid em todos os diretórios para que novos arquivos herdem o grupo
find "$DATA_DIR" -type d -exec chmod g+s {} \;

# Configurar ACL padrão para novos arquivos e diretórios
echo "Setting default ACL..."
setfacl -d -m g::rwx "$DATA_DIR"  # Grupo sempre terá rwx
setfacl -d -m o::rx "$DATA_DIR"   # Outros terão apenas leitura e execução
setfacl -m g::rwx "$DATA_DIR"     # Aplicar imediatamente para arquivos já existentes

# Exibir status final
echo "Permissions successfully applied!"
ls -ld "$DATA_DIR"
