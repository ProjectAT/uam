Autotested Results for {{ result.name }}
Generated at {{ result.date }}
--

Summary of Results: {{ result.results | length }} assignments graded

{% for test in result.results %}{% if test.results %}{{ test.students | studentlist('%s', ['student_id']) | join(', ') | ljust(20) }}: {{ test.results | getallcounts(0) }}/{{ test.results | getallcounts(3) }} passed
{% endif %}{% endfor %}
