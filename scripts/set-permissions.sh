#!/bin/sh
# Define the shared group name
GROUP_NAME=${DATA_GROUP:-appdata}
DATA_DIR=${DATA_ROOT_DIR}

# Ensure the DATA_DIR variable is set
if [ -z "$DATA_DIR" ]; then
    echo "Error: DATA_ROOT_DIR is not set."
    exit 1
fi

# Create the main "appdata" group if it does not exist
if ! getent group "$GROUP_NAME" >/dev/null; then
    echo "Creating group $GROUP_NAME with GID $DATA_GID..."
    addgroup --gid "$DATA_GID" "$GROUP_NAME"
fi

# Create users with their own groups and add them to the shared group
for USER_INFO in $USERS; do
    USER=$(echo "$USER_INFO" | cut -d':' -f1)
    USER_UID=$(echo "$USER_INFO" | cut -d':' -f2)

    # Create a group with the same GID as the user's UID (if it doesn’t exist)
    if ! getent group "$USER" >/dev/null; then
        echo "Creating group $USER with GID $USER_UID..."
        addgroup --gid "$USER_UID" "$USER"
    fi

    # Create the user with the same UID and primary group
    if ! id "$USER" >/dev/null 2>&1; then
        echo "Creating user $USER with UID $USER_UID and primary group $USER..."
        adduser -D -u "$USER_UID" -G "$USER" "$USER"
    fi

    # Ensure the user is added to the shared "appdata" group
    echo "Adding $USER to group $GROUP_NAME..."
    addgroup "$USER" "$GROUP_NAME"
done

# Set the group ownership of the shared directory
echo "Setting group '$GROUP_NAME' for $DATA_DIR..."
chown -R :"$GROUP_NAME" "$DATA_DIR"

# Set permissions to 2775 (setgid activated for group inheritance)
chmod -R 2775 "$DATA_DIR"

# Ensure new files inherit group ownership
find "$DATA_DIR" -type d -exec chmod g+s {} \;

# Configure default ACL to ensure permission inheritance
echo "Setting default ACL..."
setfacl -d -m g::rwx "$DATA_DIR"  # Group always has rwx
setfacl -d -m o::rx "$DATA_DIR"   # Others have only read and execute
setfacl -m g::rwx "$DATA_DIR"     # Apply immediately to existing files

# Display final status
echo "Permissions successfully applied!"
ls -ld "$DATA_DIR"
