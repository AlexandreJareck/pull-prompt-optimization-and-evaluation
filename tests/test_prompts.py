"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_V2_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompt_v2() -> dict:
    """Carrega o prompt v2 do arquivo YAML."""
    with open(PROMPT_V2_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestPrompts:

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        data = load_prompt_v2()
        assert "system_prompt" in data, "Campo 'system_prompt' não encontrado no YAML"
        assert data["system_prompt"], "Campo 'system_prompt' está vazio"
        assert len(data["system_prompt"].strip()) > 50, (
            "system_prompt parece muito curto para ser útil"
        )

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        data = load_prompt_v2()
        system_prompt = data.get("system_prompt", "").lower()

        role_keywords = ["você é", "voce é", "você e um", "you are", "product manager", "especialista", "assistente especializado"]
        has_role = any(keyword in system_prompt for keyword in role_keywords)

        assert has_role, (
            "O system_prompt não define uma persona/role. "
            "Inclua algo como 'Você é um Product Manager...'"
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        data = load_prompt_v2()
        system_prompt = data.get("system_prompt", "").lower()

        format_keywords = [
            "markdown", "user story", "como ", "quero ", "para que",
            "critérios de aceitação", "criterios de aceitacao", "formato"
        ]
        has_format = any(keyword in system_prompt for keyword in format_keywords)

        assert has_format, (
            "O system_prompt não menciona um formato de saída esperado. "
            "Inclua instruções de formato (Markdown, User Story, Critérios de Aceitação, etc.)"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        data = load_prompt_v2()
        system_prompt = data.get("system_prompt", "").lower()

        # Verifica presença de marcadores típicos de few-shot
        few_shot_markers = [
            "exemplo", "example", "entrada", "saída", "saida",
            "input", "output", "relato de bug:", "user story:"
        ]
        matches = sum(1 for marker in few_shot_markers if marker in system_prompt)

        assert matches >= 3, (
            f"O prompt parece não conter exemplos Few-shot suficientes "
            f"(encontrados {matches} marcadores, esperado >= 3). "
            "Inclua pelo menos 2 exemplos completos de entrada/saída."
        )

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum [TODO] no texto."""
        data = load_prompt_v2()
        full_text = yaml.dump(data, allow_unicode=True)

        assert "[TODO]" not in full_text, "Encontrado '[TODO]' no prompt — remova antes de publicar"
        assert "TODO" not in full_text or "TODO" not in data.get("system_prompt", ""), (
            "Encontrado 'TODO' no system_prompt — remova antes de publicar"
        )

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        data = load_prompt_v2()

        techniques = data.get("techniques_applied", [])

        assert isinstance(techniques, list), (
            "O campo 'techniques_applied' deve ser uma lista no YAML"
        )
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas em 'techniques_applied', "
            f"encontradas: {len(techniques)}. Técnicas atuais: {techniques}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
