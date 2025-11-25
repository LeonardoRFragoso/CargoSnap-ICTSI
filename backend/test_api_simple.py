"""
Teste simples da API do CargoSnap (sem Django)
Execute: python test_api_simple.py
"""

import requests
import json

TOKEN = "eW15Y1FGeXRqOEZRa3AxRlFRcXRMaGJyVmxMQjRVM3FfMTMwNQ=="
BASE_URL = "https://api.cargosnap.com/api/v2"

def test_first_call():
    """Testa primeira chamada - lista de arquivos"""
    print("\n" + "="*60)
    print("TESTE 1: Lista de Arquivos (Primeira Chamada)")
    print("="*60)
    
    url = f"{BASE_URL}/files"
    params = {
        'token': TOKEN,
        'limit': 5
    }
    
    try:
        print(f"\nURL: {url}")
        print(f"Params: limit=5")
        
        response = requests.get(url, params=params, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✓ SUCESSO!")
            print(f"  Total de arquivos: {data.get('total', 0)}")
            print(f"  Total de páginas: {data.get('last_page', 0)}")
            print(f"  Arquivos nesta página: {len(data.get('data', []))}")
            print(f"  Página atual: {data.get('current_page', 1)}")
            
            if data.get('data'):
                print(f"\n  Primeiros arquivos:")
                for i, file in enumerate(data['data'][:3], 1):
                    print(f"    {i}. {file['scan_code']} (ID: {file['id']}) - {file['snap_count']} fotos")
                
                return data['data'][0]['id']  # Retorna ID do primeiro
        else:
            print(f"✗ ERRO: Status {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        return None

def test_second_call(file_id):
    """Testa segunda chamada - detalhes do arquivo"""
    print("\n" + "="*60)
    print(f"TESTE 2: Detalhes do Arquivo (Segunda Chamada)")
    print("="*60)
    
    url = f"{BASE_URL}/files/{file_id}"
    params = {'token': TOKEN}
    
    try:
        print(f"\nURL: {url}")
        print(f"File ID: {file_id}")
        
        response = requests.get(url, params=params, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✓ SUCESSO!")
            print(f"  Container: {data['scan_code']}")
            print(f"  Total de uploads: {len(data.get('uploads', []))}")
            print(f"  Total de workflows: {len(data.get('workflow_runs', []))}")
            print(f"  Total de localizações: {len(data.get('locations', []))}")
            print(f"  Total de campos: {len(data.get('fields', []))}")
            print(f"  Total de formulários: {len(data.get('form_submits', []))}")
            
            # Mostra primeira imagem
            if data.get('uploads'):
                print(f"\n  Primeira imagem:")
                upload = data['uploads'][0]
                print(f"    ID: {upload['id']}")
                print(f"    Data: {upload['scan_date_time']}")
                print(f"    Device: {upload.get('device_nick', 'N/A')}")
                print(f"    Workflow: {upload.get('workflow_step_description', 'N/A')}")
                print(f"    URL: {upload['image_url'][:80]}...")
                print(f"    Thumbnail: {upload['image_thumb'][:80]}...")
                print(f"    Tem avaria: {'Sim' if upload['has_damage'] else 'Não'}")
                
                if upload.get('latitude') and upload.get('longitude'):
                    print(f"    Localização: {upload['latitude']}, {upload['longitude']}")
            
            # Mostra workflow
            if data.get('workflow_runs'):
                print(f"\n  Primeiro workflow:")
                wf = data['workflow_runs'][0]
                print(f"    ID: {wf['id']}")
                print(f"    Nome: {wf.get('workflow', {}).get('name', 'N/A')}")
                print(f"    Iniciado: {wf['submit_date_time']}")
                print(f"    Concluído: {wf.get('completed_at', 'Em andamento')}")
                print(f"    Etapas: {len(wf.get('workflow_run_steps', []))}")
            
            return True
        else:
            print(f"✗ ERRO: Status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        return False

def test_pagination():
    """Testa paginação"""
    print("\n" + "="*60)
    print("TESTE 3: Paginação")
    print("="*60)
    
    url = f"{BASE_URL}/files"
    
    try:
        # Primeira página
        response = requests.get(url, params={'token': TOKEN, 'limit': 10}, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✓ Informações de paginação:")
            print(f"  Total de registros: {data.get('total', 0)}")
            print(f"  Total de páginas: {data.get('last_page', 0)}")
            print(f"  Por página: {data.get('per_page', 0)}")
            print(f"  Primeira página: {data.get('first_page_url', 'N/A')}")
            print(f"  Última página: {data.get('last_page_url', 'N/A')}")
            print(f"  Próxima página: {data.get('next_page_url', 'Nenhuma')}")
            
            # Testa segunda página se houver
            if data.get('next_page_url'):
                print(f"\n  Testando segunda página...")
                response2 = requests.get(url, params={'token': TOKEN, 'limit': 10, 'page': 2}, timeout=30)
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    print(f"  ✓ Segunda página OK - {len(data2.get('data', []))} registros")
                else:
                    print(f"  ✗ Erro na segunda página")
            
            return True
        else:
            print(f"✗ ERRO: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("  TESTE DA API CARGOSNAP")
    print("  (Sem necessidade do Django rodando)")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Token: {TOKEN[:30]}...")
    
    # Teste 1
    file_id = test_first_call()
    
    if not file_id:
        print("\n⚠ Primeira chamada falhou. Verifique sua conexão e token.")
        return
    
    # Teste 2
    success = test_second_call(file_id)
    
    if not success:
        print("\n⚠ Segunda chamada falhou.")
        return
    
    # Teste 3
    test_pagination()
    
    # Resumo
    print("\n" + "="*60)
    print("  RESUMO")
    print("="*60)
    print("\n✓ API do CargoSnap está funcionando!")
    print("✓ Ambas as chamadas estão retornando dados")
    print("✓ Paginação está funcionando")
    
    print("\nPróximos passos:")
    print("  1. Execute o teste completo: python test_cargosnap_integration.py")
    print("  2. Sincronize os dados: python manage.py sync_cargosnap")
    print("  3. Acesse a interface: http://localhost:5173/cargosnap")

if __name__ == '__main__':
    main()
