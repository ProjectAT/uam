*/,
* Grades for {{ result.name }} at {{ result.date }}
* Summary of Results: {{ result.results | length }} assignments graded
utorid " ! , 9
{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure', 'initializationError'])) %}{{ test | to_gf_names }} / 1
{% endfor %}total ={% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure', 'initializationError'])) %} {{ test | to_gf_names }} : 1{% endfor %}

{% for group in result.results %}{% for student in group.students %}{{ student.student_number }}  {% if student.student_number == '0000000000' %}m{% else %} {% endif %} {{ student.first }} {{ student.last }},{{ student.student_id }}{% for test in (result.tests | exclude(['unittest.loader.ModuleImportFailure', 'initializationError'])) %},{{ test | passed(group.results) }}{% endfor %}
{% endfor %}{% endfor %}
