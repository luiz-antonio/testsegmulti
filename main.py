#!/usr/bin/env python3
import asyncio
import logging
import os


def get_commands():
    return [
        "python --version",
        "ls -y",
        "pwd",
        "ls -l"
    ]


def get_log_dir():
    return '/var/log/testsegmulti/'


def get_log_file_name():
    return 'testsegmulti_main.log'


def set_log_config():
    if not os.path.exists(get_log_dir()):
        try:
            os.makedirs(get_log_dir())
        except OSError as err:
            print('Erro ao criar o diretorio de LOG: {msg}'.format(msg=err.strerror))
            print('Tente executar com SUDO ou crie o diretorio {dirname} previamente.'.format(dirname= get_log_dir()))

    logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s ; %(filename)s ; %(funcName)s ; %(process)d ; %(levelname)s ; %(message)s',
                        filename=get_log_dir() + get_log_file_name(),
                        encoding='utf-8',
                        filemode='w',
                        level=logging.INFO)


async def my_run(cmd):
    logging.info('Start running "$ {cmd}" '.format(cmd=cmd))
    proc = await asyncio.create_subprocess_shell(
        cmd ,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    logging.info('Stop Running "$ {cmd}"'.format(cmd=cmd))
    stdout, stderr = await proc.communicate()
    if stderr:
        logging.error(stderr)
    #print("Erros =>", cmd, stderr)
    #print("saida =>", cmd, stdout)


def run_my_commands():
    for cmd in get_commands():
        asyncio.run(my_run(cmd))


def main():
    set_log_config()
    logging.info('Started')
    run_my_commands()
    logging.info('Finished')


if __name__ == '__main__':
    main()

