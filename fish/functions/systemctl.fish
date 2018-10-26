# Defined in - @ line 0
function systemctl --description 'alias systemctl sudo systemctl'
	sudo systemctl $argv;
end
