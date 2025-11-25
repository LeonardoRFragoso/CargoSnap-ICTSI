"""
Script para testar paginação da API do CargoSnap
Execute: python test_pagination.py
"""

import requests

TOKEN = "eW15Y1FGeXRqOEZRa3AxRlFRcXRMaGJyVmxMQjRVM3FfMTMwNQ=="
BASE_URL = "https://api.cargosnap.com/api/v2"

def test_pagination_with_limit(limit):
    """Testa paginação com um limite específico"""
    print(f"\n{'='*70}")
    print(f"  TESTANDO COM LIMIT={limit}")
    print(f"{'='*70}")
    
    url = f"{BASE_URL}/files"
    params = {
        'token': TOKEN,
        'limit': limit,
        'page': 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        total = data.get('total', 0)
        current_page = data.get('current_page', 1)
        last_page = data.get('last_page', 1)
        per_page = data.get('per_page', 0)
        files_in_page = len(data.get('data', []))
        
        print(f"\n📊 Informações de Paginação:")
        print(f"  ├─ Total de registros: {total}")
        print(f"  ├─ Registros por página: {per_page}")
        print(f"  ├─ Total de páginas: {last_page}")
        print(f"  ├─ Página atual: {current_page}")
        print(f"  └─ Arquivos nesta página: {files_in_page}")
        
        if last_page > 1:
            print(f"\n✅ MÚLTIPLAS PÁGINAS DETECTADAS!")
            print(f"   Com limit={limit}, existem {last_page} páginas")
            
            # Testa segunda página
            print(f"\n   Testando página 2...")
            params['page'] = 2
            response2 = requests.get(url, params=params, timeout=30)
            if response2.status_code == 200:
                data2 = response2.json()
                files_p2 = len(data2.get('data', []))
                print(f"   ✓ Página 2 OK - {files_p2} arquivos")
            
            # Testa última página
            if last_page > 2:
                print(f"\n   Testando última página ({last_page})...")
                params['page'] = last_page
                response_last = requests.get(url, params=params, timeout=30)
                if response_last.status_code == 200:
                    data_last = response_last.json()
                    files_last = len(data_last.get('data', []))
                    print(f"   ✓ Última página OK - {files_last} arquivos")
        else:
            print(f"\n⚠️  Apenas 1 página encontrada com limit={limit}")
        
        return {
            'limit': limit,
            'total': total,
            'pages': last_page,
            'per_page': per_page
        }
        
    except Exception as e:
        print(f"\n✗ ERRO: {str(e)}")
        return None

def main():
    print("\n" + "="*70)
    print("  TESTE DE PAGINAÇÃO - API CARGOSNAP")
    print("="*70)
    print("\nVamos testar com diferentes valores de 'limit' para ver")
    print("quantas páginas existem em cada configuração.\n")
    
    # Testa com diferentes limites
    limits_to_test = [5, 10, 20, 25, 50, 100]
    results = []
    
    for limit in limits_to_test:
        result = test_pagination_with_limit(limit)
        if result:
            results.append(result)
    
    # Resumo
    print(f"\n{'='*70}")
    print("  RESUMO DOS TESTES")
    print(f"{'='*70}\n")
    
    print(f"{'Limit':<10} {'Total':<10} {'Páginas':<10} {'Por Página':<15}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['limit']:<10} {r['total']:<10} {r['pages']:<10} {r['per_page']:<15}")
    
    # Análise
    print(f"\n{'='*70}")
    print("  ANÁLISE")
    print(f"{'='*70}")
    
    if results:
        total_records = results[0]['total']
        print(f"\n📦 Total de registros na API: {total_records}")
        
        print(f"\n💡 Recomendação:")
        print(f"   Para processar todos os dados, você pode:")
        
        # Encontra o limit que dá mais páginas
        max_pages_result = max(results, key=lambda x: x['pages'])
        
        if max_pages_result['pages'] > 1:
            print(f"\n   1. Usar limit={max_pages_result['limit']} → {max_pages_result['pages']} páginas")
            print(f"      Comando: python manage.py sync_cargosnap")
            print(f"      (O sistema usará o limit padrão)")
            
            # Calcula melhor estratégia
            best_limit = 10  # Um bom equilíbrio
            pages_with_best = (total_records + best_limit - 1) // best_limit
            
            print(f"\n   2. Ou usar limit={best_limit} → ~{pages_with_best} páginas")
            print(f"      Isso dará mais feedback durante o processo")
        else:
            print(f"\n   Todos os {total_records} registros cabem em 1 página")
            print(f"   com qualquer limit >= {total_records}")
    
    print(f"\n{'='*70}\n")

if __name__ == '__main__':
    main()
