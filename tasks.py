from invoke import task

@task
def run_once(c):
    c.run("python src/main_scheduler.py --once")

@task
def run_date(c, date="2025-06-10"):
    c.run(f"python src/main_scheduler.py --date_from={date} --once")

@task
def dashboard(c):
    c.run("streamlit run dashboard/main.py")

@task
def test(c):
    c.run("pytest tests/")
