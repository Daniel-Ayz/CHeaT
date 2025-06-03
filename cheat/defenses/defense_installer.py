import os
import shutil
import stat

class DefenseInstaller:
    def __init__(self, logger):
        self.logger = logger

    def check_permissions(self, asset_path):
        """
        Checks if the program has sufficient permissions to:
        1. Move the binary to _original.
        2. Write a new binary in its place.
        3. Set ownership of the new binary to match the original binary.
        4. Set permissions of the new binary to match the original binary.
        This is done by enumerating the file's metadata and current process capabilities.
        """
        try:
            # Get the current permissions and ownership of the asset
            asset_stat = os.stat(asset_path)
            asset_uid = asset_stat.st_uid
            asset_gid = asset_stat.st_gid
            asset_mode = stat.S_IMODE(asset_stat.st_mode)

            # Check if we can rename the binary
            # To rename, we need write and execute permissions on the containing directory
            asset_dir = os.path.dirname(asset_path)
            if not os.access(asset_dir, os.W_OK | os.X_OK):
                raise PermissionError(f"Cannot rename binary: insufficient permissions on directory {asset_dir}.")

            # Check if we can write a new binary in its place
            # Requires write permissions on the directory
            if not os.access(asset_dir, os.W_OK):
                raise PermissionError(f"Cannot write a new binary: insufficient permissions on directory {asset_dir}.")

            # Check if we can set ownership to match the original binary
            # Requires root privileges if we are not the owner of the file
            if os.geteuid() != 0 and (os.geteuid() != asset_uid or os.getegid() != asset_gid):
                raise PermissionError(
                    f"Cannot set ownership: process must run as root or match the file owner (UID: {asset_uid})."
                )

            # Check if we can set permissions to match the original binary
            # Requires write permissions on the file or directory
            if not os.access(asset_path, os.W_OK):
                raise PermissionError(f"Cannot set permissions: insufficient write permissions on {asset_path}.")

            self.logger.info(
                f"Permissions check passed for {asset_path}. "
                f"Mode: {oct(asset_mode)}, UID: {asset_uid}, GID: {asset_gid}"
            )
            return True
        except PermissionError as pe:
            self.logger.error(f"Permission error: {str(pe)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during permission check: {str(e)}")
            return False

    def install_defense(self, asset_type, asset_path, defense_obj):
        """
        Installs the defense by adding the prefix and suffix to the asset.
        """
        try:
            # Check permissions before proceeding
            if not self.check_permissions(asset_path):
                self.logger.error(f"Insufficient permissions for installing defense on: {asset_path}")
                return False
        
            prefix = defense_obj.get("prefix", "")
            suffix = defense_obj.get("suffix", "")

            if asset_type == "local_file":
                self._write_prefix_suffix_to_file(asset_path, prefix, suffix)
            elif asset_type == "web_file":
                self._write_prefix_suffix_to_file(asset_path, prefix, suffix)
            elif asset_type == "tool_wrapper":
                self._create_tool_wrapper_with_prefix_suffix(asset_path, prefix, suffix)
            else:
                raise ValueError(f"Unknown asset type: {asset_type}")

            self.logger.info(f"Defense successfully installed on {asset_path} of type {asset_type}.")
            return True
        except Exception as e:
            self.logger.info(f"Failed to install defense: {str(e)}")
            return False

    def remove_defense(self, asset_type, asset_path, defense_obj):
        """
        Removes a previously installed defense based on asset type and path.
        """
        try:
            # Check permissions before proceeding
            if not self.check_permissions(asset_path):
                self.logger.error(f"Insufficient permissions for installing defense on: {asset_path}")
                return False
        
            prefix = defense_obj.get("prefix", "")
            suffix = defense_obj.get("suffix", "")

            if asset_type == "local_file" or asset_type == "web_file":
                self._remove_prefix_suffix_from_file(asset_path, prefix, suffix)
            elif asset_type == "tool_wrapper":
                self._restore_tool(asset_path)
            else:
                raise ValueError(f"Unknown asset type: {asset_type}")

            self.logger.info(f"Defense successfully removed from {asset_path} of type {asset_type}.")
            return True
        except Exception as e:
            self.logger.info(f"Failed to remove defense: {str(e)}")
            return False

    def _write_prefix_suffix_to_file(self, file_path, prefix, suffix):
        """
        Adds the prefix at the beginning and the suffix at the end of a file.
        """
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            content = f"{prefix}{content}{suffix}"

            with open(file_path, 'w') as file:
                file.write(content)

            self.logger.info(f"Prefix and suffix added to file: {file_path}")
        except Exception as e:
            self.logger.info(f"Failed to write prefix and suffix to file: {str(e)}")

    def _create_tool_wrapper_with_prefix_suffix(self, tool_path, prefix, suffix):
        """
        Creates a wrapper script for a tool to inject a prefix and suffix defense,
        preserving the original permissions and ownership, and ensuring the original binary
        is kept in the same directory as the wrapper.
        """
        try:
            # Generate the path for the original binary
            original_path = f"{tool_path}_original"
            absolute_original_path = os.path.abspath(original_path)  # Resolve full absolute path

            # Rename the original binary to the new location
            os.rename(tool_path, original_path)

            # Get the original binary's permissions and ownership
            original_stat = os.stat(original_path)
            original_mode = stat.S_IMODE(original_stat.st_mode)  # File permissions
            original_uid = original_stat.st_uid  # User ID
            original_gid = original_stat.st_gid  # Group ID

            # Create the new wrapper binary in the same location
            with open(tool_path, 'w') as file:
                file.write("#!/bin/bash\n")
                file.write(f"echo \"{prefix}\"\n")
                file.write(f"{absolute_original_path} \"$@\"\n")  # Use absolute path
                file.write(f"echo \"{suffix}\"\n")

            # Set the ownership of the new wrapper binary to match the original
            shutil.chown(tool_path, user=original_uid, group=original_gid)

            # Set the permissions of the new wrapper binary to match the original
            os.chmod(tool_path, original_mode)

            self.logger.info(f"Tool wrapper with prefix and suffix created: {tool_path}")
        except Exception as e:
            self.logger.error(f"Failed to create tool wrapper: {str(e)}")

    def _remove_prefix_suffix_from_file(self, file_path, prefix, suffix):
        """
        Removes specific prefix and suffix content from a file.
        """
        try:
            # Read the entire file content as a single string
            with open(file_path, 'r') as file:
                content = file.read()

            # Remove prefix if it matches the start of the content
            if content.startswith(prefix):
                content = content[len(prefix):]

            # Remove suffix if it matches the end of the content
            if content.endswith(suffix):
                content = content[:-len(suffix)]

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(content)

            self.logger.info(f"Prefix and suffix removed from file: {file_path}")
        except Exception as e:
            self.logger.info(f"Failed to remove prefix and suffix from file: {str(e)}")


    def _restore_tool(self, tool_path):
        """
        Restores the original tool by removing the wrapper.
        """
        try:
            original_path = f"{tool_path}_original"
            if os.path.exists(original_path):
                os.rename(original_path, tool_path)
                self.logger.info(f"Restored original tool from wrapper: {tool_path}")
            else:
                self.logger.info(f"Original tool not found for wrapper: {tool_path}")
        except Exception as e:
            self.logger.info(f"Failed to restore tool: {str(e)}")
