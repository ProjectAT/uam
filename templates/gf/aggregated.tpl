*/,
* Grades for {{ result.name }} at {{ result.date }}
* Summary of Results: {{ result.results | length }} assignments graded
utorid " ! , 9
{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure'])) %}{{ test | togfnames }} / 1
{% endfor %}total ={% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure'])) %} {{ test | togfnames }} : {{ result.tests | exclude(['unittest.loader.ModuleImportFailure']) | getbalancedweight }}{% endfor %}

{% for group in result.results %}{% for student in group.students %}{{ student.student_number }}  {% if student.student_number == '0000000000' %}m{% else %} {% endif %} {{ student.first }} {{ student.last }},{{ student.student_id }}{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure'])) %},{{ test | passed(group.results) }}{% endfor %}
{% endfor %}{% endfor %}
