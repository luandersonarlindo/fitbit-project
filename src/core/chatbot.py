# core/chatbot/rules.py

def answer_intent(intent, user_data):
    """
    Retorna a resposta do chatbot com base na intenção e nos dados do usuário.

    Parâmetros:
    - intent: str, a intenção detectada na pergunta do usuário
    - user_data: dict, dados reais do usuário (calorias, passos, minutos ativos, etc.)

    Retorna:
    - str: resposta do chatbot
    """
    
    if intent == "calories_today":
        calories = user_data.get("Calories", 0)
        return f"Hoje você queimou aproximadamente {calories} calorias."

    elif intent == "steps_today":
        steps = user_data.get("TotalSteps", 0)
        return f"Hoje você deu {steps} passos."

    elif intent == "active_minutes":
        active_minutes = user_data.get("ActiveMinutes", 0)
        return f"Você esteve ativo por {active_minutes} minutos hoje."

    elif intent == "active_patterns":
        # Resposta detalhada sobre padrões de usuários ativos
        return (
            "Usuários mais ativos tendem a apresentar os seguintes padrões:\n"
            "- Maior quantidade de minutos em atividades muito e moderadamente ativas\n"
            "- Menor quantidade de tempo sedentário\n"
            "- Maior número de passos diários e distância percorrida\n"
            "- Consumo calórico diário geralmente mais elevado"
        )

    elif intent == "help":
        return (
            "Você pode perguntar sobre:\n"
            "- Calorias queimadas hoje\n"
            "- Passos dados hoje\n"
            "- Minutos de atividade hoje\n"
            "- Padrões de usuários mais ativos"
        )

    else:
        return "Desculpe, não entendi sua pergunta. Tente reformular ou digite 'ajuda'."
