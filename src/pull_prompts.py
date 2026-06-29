"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prompts_dir = os.path.join(project_root, "prompts")


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt v1 do LangSmith Hub e salva localmente em YAML.
    """
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    save_path = os.path.join(prompts_dir, "bug_to_user_story_v1.yml")

    print(f"   Puxando prompt: {prompt_name}")

    try:
        prompt = hub.pull(prompt_name)

        # Extrai os dados relevantes do prompt para salvar em YAML limpo
        messages = prompt.messages
        system_content = ""
        human_content = ""

        for msg in messages:
            template = msg.prompt.template if hasattr(msg, "prompt") else ""
            class_name = type(msg).__name__
            if "System" in class_name:
                system_content = template
            elif "Human" in class_name:
                human_content = template

        # Tenta extrair input_variables
        input_vars = list(prompt.input_variables) if hasattr(prompt, "input_variables") else ["bug_report"]

        prompt_data = {
            "name": "bug_to_user_story_v1",
            "version": "1.0",
            "description": "Prompt original (baixa qualidade) — base para otimização",
            "input_variables": input_vars,
            "system_prompt": system_content,
            "human_prompt": human_content,
            "metadata": {
                "source": f"https://smith.langchain.com/hub/{prompt_name}",
                "pulled_from": prompt_name,
            }
        }

        os.makedirs(prompts_dir, exist_ok=True)
        success = save_yaml(prompt_data, save_path)

        if success:
            print(f"   ✓ Prompt salvo em: {save_path}")
        else:
            print(f"   ❌ Erro ao salvar prompt em: {save_path}")

        return success

    except Exception as e:
        print(f"   ❌ Erro ao fazer pull do prompt '{prompt_name}': {e}")
        print("\n   Verifique:")
        print("   - LANGSMITH_API_KEY está correta no .env")
        print("   - Você tem acesso ao LangSmith Hub")
        print("   - Sua conexão com a internet está funcionando")
        return False


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_env_vars = [
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
        "USERNAME_LANGSMITH_HUB",
    ]

    if not check_env_vars(required_env_vars):
        return 1

    success = pull_prompts_from_langsmith()

    if success:
        print("\n✅ Pull concluído com sucesso!")
        print("\nPróximo passo:")
        print("   Edite prompts/bug_to_user_story_v2.yml com seu prompt otimizado")
        print("   Depois execute: python src/push_prompts.py")
        return 0
    else:
        print("\n❌ Pull falhou. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
