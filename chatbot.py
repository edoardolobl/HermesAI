from models import User, CEFRAssessment, PersonalityAssessment, LearningPath, ExerciseGenerator


class Chatbot:
    """
    Interface principal do usuário, gerenciando a interação com o sistema.
    """

    def __init__(self):
        """
        Inicializa um objeto Chatbot e carrega os dados do usuário.
        """
        self.user = User()
        self.user.load_data()

    def display_menu(self):
        """
        Exibe o menu principal do chatbot.
        """
        user_name = self.user.name or "usuário"

        print(f"\nOlá, {user_name}! Bem-vindo ao Hermes AI Language Assistant! 👋")
        print("-----------------------------------------")
        print("Seu companheiro personalizado para o aprendizado de idiomas. 🌎📚")

        print("\nSiga as opções na ordem para uma experiência completa! 🚀\n")
        print("1. Registre seu nome para uma experiência personalizada. 📝")
        print("2. Faça o teste de nível CEFR para descobrir seu nível de proficiência. 📈")
        print("3. Descubra seu perfil de aprendiz com o Teste de Personalidade. 🤔")
        print("4. Receba um plano de estudos personalizado com base em seu nível e perfil. 🗺️")
        print("5. Explore exemplos de exercícios para praticar o idioma. 💪")
        print("6. Sair. 👋")

    def handle_user_input(self):
        """
        Processa a entrada do usuário e executa a ação correspondente.
        """
        while True:
            print("\n-----------------------------------------")
            option = input("Escolha uma opção (0 para exibir o menu novamente): ")

            if option == '0':
                self.display_menu()

            elif option == '1':
                user_name = str(input("Informe seu nome: "))
                self.user.name = user_name
                print(f"Nome registrado com sucesso!")
                self.user.save_data()

            elif option == '2':
                language = input(
                    "Escolha o idioma (Inglês, Italiano, Francês, Alemão, Espanhol): "
                )
                self.user.language = language
                cefr_assessment = CEFRAssessment(language)
                cefr_assessment.generate_questions()
                cefr_assessment.administer_test()
                evaluation_result = cefr_assessment.evaluate_performance()
                print(f"Resultado da Avaliação: {evaluation_result}")
                self.user.cefr_level = evaluation_result
                self.user.save_data()

            elif option == '3':
                personality_assessment = PersonalityAssessment(self.user.language)
                personality_assessment.generate_questions()
                personality_assessment.administer_test()
                personality_result = personality_assessment.evaluate_performance()
                print(f"Resultado do Teste de Personalidade: {personality_result}")
                self.user.personality_profile = personality_result
                self.user.save_data()

            elif option == '4':
                if self.user.name:
                    learning_path = LearningPath(self.user)
                    learning_plan = learning_path.generate_learning_plan()
                    print(f"\nPlano de Estudos Personalizado para {self.user.name}:\n{learning_plan}")
                    self.user.save_data()
                else:
                    print("Por favor, registre seu nome primeiro (Opção 1).")

            elif option == '5':
                if self.user.name:
                    exercise_generator = ExerciseGenerator(self.user)
                    exercises = exercise_generator.generate_exercises()
                    print(
                        f"\nExemplos de Exercícios para {self.user.name}:\n{exercises}"
                    )
                else:
                    print("Por favor, registre seu nome primeiro (Opção 1).")

            elif option == '6':
                print("Obrigado por usar o HermesAI!")
                break

            else:
                print("Opção inválida, tente novamente!")

    def run(self):
        """
        Inicia a execução do chatbot.
        """
        self.display_menu()
        self.handle_user_input()


if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
