Autotested Results for {{ result.assignment }} submitted by {{ result.students | student_list('%s %s (%s)', ['first', 'last', 'student_id']) | join(', ') }}
Generated at {{ result.date }}

Summary of Results: {{ result.results | get_all_counts(0) }} out of {{ result.results | get_all_counts(3) }} tests successfully passed
--

{% for test in result.results %}{% set test_num = [0] %}Tests for {{ test }} ({{ result.results[test] | get_counts(0) }}/{{ result.results[test] | get_counts(3) }} passed)
--

{% for method in result.results[test].passes %}{% do test_num.insert(0, test_num[0] + 1) %}{% do test_num.pop() %}{{ test_num[0] }}) {{ ((result.results[test].passes[method] or method) | wordwrap) | ljust(82, 3) }} .. ok!
{% endfor %}{% for method in result.results[test].failures %}{% do test_num.insert(0, test_num[0] + 1) %}{% do test_num.pop() %}{{ test_num[0] }}) {{ ((result.results[test].failures[method].description or method) | wordwrap) | ljust(82, 3) }} .. failed
.. because {{ result.results[test].failures[method].message }}


{% endfor %}{% for method in result.results[test].errors %}{% do test_num.insert(0, test_num[0] + 1) %}{% do test_num.pop() %}{{ test_num[0] }}) {{ ((result.results[test].errors[method].description or method) | wordwrap) | ljust(82, 3) }} .. error
.. because {{ result.results[test].errors[method].message }}

{% endfor %}

{% endfor %}
