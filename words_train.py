
class WordsTrain:
    def __init__(self):
        # Labels possíveis
        self.labels = ["Produtivo", "Improdutivo"]


        # Labels possíveis
        self.labels = ["Produtivo", "Improdutivo"]

        # Exemplos para few-shot / prompt contextual
        self.example_texts = [
            ("Favor enviar planilha de acompanhamento das entregas.", "Produtivo"),
            ("Lembrete: reunião semanal às 10h.", "Produtivo"),
            ("Precisamos revisar o orçamento antes da aprovação.", "Produtivo"),
            ("Confirme se recebeu o contrato assinado.", "Produtivo"),
            ("A entrega do projeto deve ser finalizada até amanhã.", "Produtivo"),
            ("Parabéns pelo excelente trabalho no evento!", "Improdutivo"),
            ("Bom dia, espero que esteja bem!", "Improdutivo"),
            ("Segue newsletter semanal da empresa.", "Improdutivo"),
            ("Convite para o evento de confraternização.", "Improdutivo"),
            ("Informativo sobre feriado na próxima semana.", "Improdutivo")
        ]
        # Palavras-chave importantes para emails produtivos
        self.important_keywords = [
            "urgente", "urgência", "prioritário", "pendente", "pendência",
            "entregar", "entrega", "prazo", "prazos", "deadline", "deadlines",
            "finalizar", "revisar", "revisão", "atualizar", "atualização",
            "enviar", "envio", "mandar", "remeter", "fornecer", "compartilhar",
            "submeter", "solicitar", "requisitar", "pedir", "requerer",
            "report", "relatorio", "relatórios", "relatorios", "ata",
            "aprovar", "aprovação", "validar", "validação", "verificar", "encontro", "call", "teleconferência",
            "videoconferência", "alinhamento", "discussão", "debate",
            "briefing", "pauta", "agendar", "agendamento", "convocação",
            "planilha", "planilhas", "documento", "documentação", "laudo",
            "parecer", "análise", "resumo", "sumário", "formulário",
            "proposta", "orçamento", "contrato", "checagem", "conferir",
            "avaliar", "avaliação", "feedback", "revisado", "aprovado",
            "tarefa", "tarefas", "projeto", "projetos", "atividade",
            "atividades", "executar", "execução", "implementar", "implantação",
            "desenvolver", "desenvolvimento", "etapa", "fase", "marco",
            "progresso", "andamento", "status", "acompanhamento", "seguimento",
            "monitoramento", "relatar", "informar", "notificar", "notificação",
            "confirmar", "confirmação", "responder", "resposta", "retornar",
            "retorno", "aceitar", "aceitação", "rejeitar", "recusar",
            "kpi", "metricas", "métricas", "performance", "desempenho",
            "resultados", "entregáveis", "deliverable", "sprint", "backlog",
            "roadmap", "estratégia", "gestão", "operacional",
            "prioridade", "escalonar", "resolver", "solução", "ação",
            "instrução", "diretriz", "orientação", "coordenação", "suporte",
            "ajuste", "correção","urgente", "urgência", "prioritário", "pendente", "pendência",
            "entregar", "entrega", "prazo", "prazos", "deadline", "deadlines",
            "finalizar", "revisar", "revisão", "atualizar", "atualização",
            "enviar", "envio", "mandar", "remeter", "fornecer", "compartilhar",
            "submeter", "solicitar", "requisitar", "pedir", "requerer",
            "report", "relatorio", "relatórios", "relatorios", "ata"
        ]

