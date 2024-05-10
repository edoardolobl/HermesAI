import google.generativeai as genai
import json
import textwrap

model = genai.GenerativeModel('gemini-1.0-pro-latest')

class User:
    """
    Representa um usuário do sistema, armazenando suas informações e
    gerenciando a persistência dos dados.
    """

    def __init__(self, name=None, language=None, cefr_level=None, personality_profile=None):
        """
        Inicializa um objeto User com os dados fornecidos.
        """
        self.name = name
        self.language = language
        self.cefr_level = cefr_level
        self.personality_profile = personality_profile

    def save_data(self, filename="dados_aluno.json"):
        """
        Salva os dados do usuário em um arquivo JSON.
        """
        data = {
            "nome_aluno": self.name,
            "idioma": self.language,
            "nivel_cefr": self.cefr_level,
            "personalidade": self.personality_profile
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self, filename="dados_aluno.json"):
        """
        Carrega os dados do usuário de um arquivo JSON.
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.name = data.get("nome_aluno")
                self.language = data.get("idioma")
                self.cefr_level = data.get("nivel_cefr")
                self.personality_profile = data.get("personalidade")
        except FileNotFoundError:
            return



class Assessment:
    """
    Classe abstrata que define a estrutura básica para avaliações.
    """

    def __init__(self, language):
        """
        Inicializa um objeto Assessment com o idioma da avaliação.
        """
        self.language = language
        self.questions = []
        self.chat_session = genai.ChatSession(model)

    def generate_questions(self):
        """
        Método abstrato para gerar as perguntas da avaliação.
        Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError

    def administer_test(self):
        """
        Aplica o teste ao usuário, coletando as respostas.
        """
        for i, question in enumerate(self.questions):
            print(f"{i + 1}. {question}\n")
            user_answer = input()
            self.chat_session.send_message(user_answer)
        print("Respostas registradas. Obrigado!")

    def evaluate_performance(self):
        """
        Método abstrato para avaliar o desempenho do usuário na avaliação.
        Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError


class CEFRAssessment(Assessment):
    """
    Avaliação para determinar o nível CEFR do usuário em um idioma.
    """

    def __init__(self, language):
        """
        Inicializa um objeto CEFRAssessment.
        """
        super().__init__(language)
        self.levels = ["A1", "A2", "B1", "B2", "C1"]
        self.level_counts = {level: 0 for level in self.levels}

    def generate_questions(self):
        """
        Gera perguntas de teste CEFR com base no nível alvo.
        """
        for _ in range(3):
            target_level = min(self.level_counts, key=self.level_counts.get)
            prompt = f"""Crie uma pergunta de nível CEFR {target_level} para testar o nível de {self.language} de um aluno.
            A pergunta deve ser baseada em texto, sem exigir compreensão auditiva ou outros formatos.
            Não inclua a resposta da pergunta e evite perguntas triviais que possam ser respondidas com uma única palavra.
            Concentre-se em avaliar a compreensão do texto e o uso do idioma.
            """
            response = self.chat_session.send_message(prompt)
            question = textwrap.fill(response.text, width=120, replace_whitespace=False)
            self.questions.append(question)
            self.level_counts[target_level] += 1

    def evaluate_performance(self):
        """
        Avalia o histórico do chat e estima o nível CEFR do usuário.
        """
        history = self.chat_session.history
        history_text = ""
        for message in history:
            history_text += f"Pergunta: {message.parts[0].text}\n"
            if len(message.parts) > 1:
                history_text += f"Resposta: {message.parts[1].text}\n"

        prompt = f"""Analise o seguinte histórico de perguntas e respostas de um teste de nível CEFR e 
        forneça uma breve visão geral do desempenho do aluno, incluindo o nível de proficiência estimado no idioma {self.language}.
        {history_text}
        """
        evaluation_result = get_gemini_answer(prompt)
        return evaluation_result


class PersonalityAssessment(Assessment):
    """
    Avaliação para determinar o perfil de aprendizagem do usuário.
    """

    def generate_questions(self):
        """
        Gera perguntas de múltipla escolha para o teste de personalidade.
        """
        for _ in range(2):
            prompt = f"""
            Considerando o histórico da entrevista até o momento, crie uma pergunta de múltipla escolha para um teste de 
            personalidade que visa identificar o perfil de um aluno de idiomas.
            A pergunta deve explorar as motivações, objetivos e preferências de aprendizagem do aluno, oferecendo três 
            opções de cenários que reflitam diferentes perfis de aprendiz.
            Os cenários devem ser baseados nos seguintes aspectos, sem direcionar o entrevistado para categorias específicas:
            * Interesses pessoais
            * Motivações iniciais
            * Objetivos específicos
            * Preferências de métodos e abordagens
            * Desafios e barreiras
            * Importância do idioma no futuro
            * Experiências passadas
            * Recursos e ferramentas úteis
            * Interesse por culturas ou países
            * Autoavaliação de habilidades
            Evite perguntas repetitivas ou que já tenham sido abordadas. Busque cenários distintos e que representem 
            diferentes perfis de aprendiz.
            """
            response = self.chat_session.send_message(prompt)
            question = textwrap.fill(response.text, width=120, replace_whitespace=False)
            self.questions.append(question)

    def evaluate_performance(self):
        """
        Analisa o histórico do chat e gera um resumo do perfil de aprendizagem do usuário.
        """
        history = self.chat_session.history
        history_text = ""
        for message in history:
            history_text += f"Pergunta: {message.parts[0].text}\n"
            if len(message.parts) > 1:
                history_text += f"Resposta: {message.parts[1].text}\n"

        prompt = f"""
        Analise o seguinte histórico de perguntas e respostas de um teste de personalidade e, com base nas informações 
        fornecidas, gere um relatório conciso (um parágrafo) descrevendo o perfil de aprendiz de idiomas do aluno. 
        O relatório deve destacar as principais características do perfil do aluno, incluindo suas motivações, objetivos e 
        preferências de aprendizagem. Evite repetir as perguntas e respostas do histórico, focando em uma análise 
        interpretativa das informações. 
        Identifique padrões e tendências nas respostas do aluno para criar um perfil único e personalizado.
        {history_text}
        """
        analysis_result = get_gemini_answer(prompt)
        return analysis_result


def get_gemini_answer(prompt: str) -> str:
    """
    Envia um prompt para o modelo Gemini e retorna a resposta de texto gerada.

    Args:
        prompt: O prompt de texto a ser enviado ao modelo Gemini.

    Returns:
        A resposta de texto gerada pelo modelo Gemini.
    """
    response = model.generate_content(prompt)
    response_formatted = textwrap.fill(response.text, width=120, replace_whitespace=False)
    return response_formatted

class LearningPath:
    """
    Gera um plano de estudos personalizado com base nas informações do usuário.
    """

    def __init__(self, user):
        """
        Inicializa um objeto LearningPath com um objeto User.
        """
        self.user = user

    def generate_learning_plan(self):
        """
        Cria um plano de estudos personalizado para o usuário.
        """
        if not self.user.cefr_level or not self.user.personality_profile:
            return """Informações insuficientes para gerar um plano de estudos. Por favor, complete o teste CEFR e o teste 
            de personalidade."""

        prompt = f"""
        Crie um plano de estudos personalizado para {self.user.name}, um aluno de {self.user.language} com nível CEFR 
        {self.user.cefr_level} e um perfil de aprendiz {self.user.personality_profile}.
        O plano de estudos deve incluir:
        * Sugestões de recursos de aprendizagem (livros, aplicativos, sites, etc.)
        * Dicas de estudo e estratégias de aprendizagem
        * Recomendações de atividades para praticar o idioma
        * Considerações sobre as motivações, objetivos e preferências de aprendizagem do aluno
        O plano deve ser adaptado ao nível CEFR e à personalidade do aluno, fornecendo um guia prático e motivador para o 
        aprendizado do idioma.
        """
        learning_plan = get_gemini_answer(prompt)
        return learning_plan


class ExerciseGenerator:
    """
    Gera exemplos de exercícios personalizados com base nas informações do usuário.
    """

    def __init__(self, user):
        """
        Inicializa um objeto ExerciseGenerator com um objeto User.
        """
        self.user = user

    def generate_exercises(self):
        """
        Cria exemplos de exercícios adequados ao nível CEFR e à personalidade do usuário.
        """
        if not self.user.cefr_level or not self.user.personality_profile:
            return ("Informações insuficientes para gerar exemplos de exercícios. Por favor, complete o teste CEFR e o "
                    "teste de personalidade.")

        prompt = f"""
        Crie exemplos de exercícios **em {self.user.language}** para {self.user.name}, um aluno de 
        {self.user.language} com nível CEFR {self.user.cefr_level} e um perfil de aprendiz 
        {self.user.personality_profile}.

        Os exercícios devem ser adequados ao nível CEFR e à personalidade do aluno, com foco em desenvolver as habilidades 
        de Compreensão escrita, Produção escrita, Gramática e Vocabulário.

        Inclua instruções claras para cada exercício **em {self.user.language}** e forneça exemplos de como o aluno pode 
        praticar.
        """

        exercises = get_gemini_answer(prompt)
        return exercises

