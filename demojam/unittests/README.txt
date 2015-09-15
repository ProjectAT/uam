This directory (unittests) should contain a test suite for any items
that are to be tested. This test suite must named 'AllTests' and must be
contained in a directory with the same name as the item being tested, and no
other 'AllTests.java' may be within a subdirectory of the unittests directory
with the same name.

For example, if testing the item 'example' with a test suite package named
'exampletester' your test suite may be located in a directory structure like
this:
unittests/example/exampletester/

However no other 'AllTests' files may be located within any other subdirectory
of the unittests directory named 'example', so having another test suite
located in a directory structure like one of the following would not work:
unittests/example/othertestsuite/
unittests/otherdirectory/example/additionaldirectory/thirdtestsuite/

Test suites packages may share the same name as the item being tested, so
if you were testing the item 'example' with a similarly named test suite
your directory structure could be as direct as this:
unittests/example/

Finally, test suite package structure is relative to this directory (unittests)
So for example, if a test suite is located in:
unittests/example/exampletester

then the test suite must be part of the package:
example.exampletester
