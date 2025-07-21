from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from django_apscheduler.jobstores import DjangoJobStore


def populate_establishments_job():
    """
    Função que chama o nosso management command.
    """
    try:
        call_command('populate_establishments')
        print("Rotina 'populate_establishments' executada com sucesso.")
    except Exception as e:
        print(f"Erro ao executar a rotina 'populate_establishments': {e}")


def start():
    """
    Inicia o agendador e adiciona o job.
    """
    scheduler = BackgroundScheduler()
    
    # Adiciona o job para rodar.
    # 'cron' é o gatilho, que permite agendamentos complexos.
    # Este exemplo roda o job todo Domingo às 3 da manhã.

    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        populate_establishments_job,
        'cron',
        day_of_week='sun',
        hour='3',
        minute='0',
        id='populate_establishments_job_id', # ID único para o job
        replace_existing=True # Substitui o job se já existir um com o mesmo ID
    )
    
    # Para testar, você pode usar o gatilho 'interval' para rodar a cada X segundos/minutos:
    # scheduler.add_job(
    #     populate_establishments_job,
    #     'interval',
    #     minutes=30, # Roda a cada 30 minutos
    #     id='populate_establishments_job_id',
    #     replace_existing=True
    # )

    scheduler.start()