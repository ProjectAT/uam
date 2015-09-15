""{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure'])) %},{{ test | togfnames }}{% endfor %}{{ "\r" }}
""{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure'])) %},1{% endfor %}{{ "\r" }}
{% for group in result.results %}{% for student in group.students %}{{ student.student_id }}{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure'])) %},{{ test | passed(group.results) }}{% endfor %}{{ "\r" }}
{% endfor %}{% endfor %}
