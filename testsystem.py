import langs
import shutil
import testutil

LANGS = {'java8': langs.Java(), 'python': langs.Python()}

class TestSystem:
    def __init__(self):
        pass

    def _prepare(self, lang, source_code):
        executable, compile_error = lang.compile(source_code)
        if executable == '':
            return compile_error
        shutil.copy(executable, testutil.box_path())
        return None

    def _get_output(self, lang, test_input):
        testutil.write_file(testutil.box_path() + '/in', test_input)
        output, error = lang.run()
        meta = testutil.parse_meta(testutil.read_file('meta'))
        if 'status' in meta:
            return meta['status'], error
        return 'OK', output
    
    def get_output(self, lang, source_code, test_input):
        compile_error = self._prepare(lang, source_code)
        if compile_error != None:
            return 'CE', compile_error
        return self._get_output(lang, test_input)

    def _get_verdict(self, lang, test_input, test_output):
        verdict, details = self._get_output(lang, test_input)
        if verdict != 'OK':
            return verdict, details
        return ('OK', '') if details == test_output else ('WA', '')

    def get_verdicts(self, lang, source_code, tests):
        compile_error = self._prepare(lang, source_code)
        if compile_error != None:
            return 'CE', compile_error
        verdicts = dict()
        for test in tests:
            verdicts[test] = self._get_verdict(lang, testutil.read_file(test + '.in'), testutil.read_file(test + '.out'))
        return verdicts

if __name__ == '__main__':
    ts = TestSystem()
    folders = ['sol-ok', 'sol-wa', 'sol-to', 'sol-re', 'sol-ce']
    tests = ['1000', '100000']
    print(testutil.get_sample_tests('.'))
    for folder in folders:
        print(ts.get_verdicts(LANGS['java8'], testutil.read_file(folder + '/Main.java'), testutil.get_sample_tests('.')))
        print(ts.get_verdicts(LANGS['python'], testutil.read_file(folder + '/main.py'), testutil.get_sample_tests('.')))
