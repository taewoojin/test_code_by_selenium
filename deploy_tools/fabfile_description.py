from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/taewoojin/test_code_by_selenium.git'   # git repo url setting
PROJECT_NAME = 'superlists'


def deploy():
    # env.user : 서버 로그인 시 사용할 사용자명
    # env.host : 커맨드 라인에서 지정한 서버 주소
    site_folder = '/home/{0}/sites/{1}'.format(env.user, env.host)
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


# 프로젝트 구조에 맞춰 디렉토리 생성
def _create_directory_structure_if_necessary(site_folder):
    # 'database', 'source', 'static', 'virtualenv' 디렉토리 생성.
    for subfolder in ('database', 'source', 'static', 'virtualenv'):
        run('mkdir -p {0}/{1}'.format(site_folder, subfolder))


# 최신 소스를 배포 서버에 fetch/clone
def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))

    # local : subprocess.Popen을 랩핑한 것으로 capture=True로 설정하면 외부 명령의 결과를 리턴해 준다.
    # 반대로 capture=False로 설정하면 subprocess에서 결과를 리턴받지 못한다.
    # 아래의 git format은 가장 최근 로그에서 커밋 해쉬만 가져오는 명령이다.
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {0} && git reset --hard {1}'.format(source_folder, current_commit))


# settings.py 설정
def _update_settings(source_folder, site_name):
    # DEBUG, ALLOWED_HOST 설정 변경.
    # sed(file_name, 'a', 'b') : file 안에서 'a'를 찾아서 'b'로 변경. regexp 도 적용 가능.
    settings_path = source_folder + '/' + PROJECT_NAME + '/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(
        settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = [{0}]'.format(site_name)
    )

    # CSRF 보안을 위한 SECRET_KEY 생성.
    secret_key_file = source_folder + '/' + PROJECT_NAME + '/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = {0}'.format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


# set virtualenv and install requirements.txt
def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 {0}'.format(virtualenv_folder))
        run('{0}/bin/pip install -r {1}/requirements.txt'.format(virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    run('cd {0} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(source_folder))


def _update_database(source_folder):
    run('cd {0} && ../virtualenv/bin/python3 manage.py migrate --noinput'.format(source_folder))