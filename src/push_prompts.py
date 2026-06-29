"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prompts_dir = os.path.join(project_root, "prompts")


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (ex: "username/bug_to_user_story_v2")
        prompt_data: Dados do prompt carregados do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        human_prompt = prompt_data.get("human_prompt", "{bug_report}")

        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt),
        ])

        tags = prompt_data.get("tags", [])
        description = prompt_data.get("description", "")

        print(f"   Fazendo push para: {prompt_name}")
        hub.push(
            prompt_name,
            prompt_template,
            tags=tags if tags else None,
            new_repo_is_public=True,
        )

        print(f"   ✓ Push realizado com sucesso!")
        print(f"   🔗 https://smith.langchain.com/hub/{prompt_name}")
        return True

    except Exception as e:
        print(f"   ❌ Erro ao fazer push de '{prompt_name}': {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB", "")

    prompts_to_push = [
        {
            "file": os.path.join(prompts_dir, "bug_to_user_story_v2.yml"),
            "hub_name": f"{username}/bug_to_user_story_v2",
        }
    ]

    all_success = True

    for item in prompts_to_push:
        file_path = item["file"]
        hub_name = item["hub_name"]

        print(f"\n📄 Processando: {hub_name}")

        prompt_data = load_yaml(file_path)
        if not prompt_data:
            print(f"   ❌ Não foi possível carregar: {file_path}")
            all_success = False
            continue

        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print(f"   ❌ Prompt inválido:")
            for error in errors:
                print(f"      - {error}")
            all_success = False
            continue

        print(f"   ✓ Prompt válido")
        success = push_prompt_to_langsmith(hub_name, prompt_data)
        if not success:
            all_success = False

    print("\n" + "=" * 50)
    if all_success:
        print("✅ Todos os prompts foram publicados com sucesso!")
        print(f"\n🔗 Veja seus prompts em:")
        print(f"   https://smith.langchain.com/hub/{username}")
        print("\nPróximo passo:")
        print("   python src/evaluate.py")
        return 0
    else:
        print("❌ Alguns prompts falharam. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
