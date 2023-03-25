# pyubx2 Pull Request Template

## Description

Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context and, where applicable, any u-blox documentation sources you have used. List any dependencies that are required for this change.

Fixes # (issue)

## Testing

Please test all changes, however trivial, against the supplied unittest suite `tests/test_*.py`. Please describe any test cases you have amended or added to this suite to maintain >= 99% code coverage.

If you're adding new UBX message definitions for Generation 9+ devices, please check for any corresponding configuration database updates (`ubxtypes_configdb.py`).

- [ ] Test A
- [ ] Test B

## Checklist:

- [ ] I agree to abide by the code of conduct (see [CODE_OF_CONDUCT.md](https://github.com/semuconsulting/pyubx2/blob/master/CODE_OF_CONDUCT.md)).
- [ ] My code follows the style guidelines of this project (see [CONTRIBUTING.MD](https://github.com/semuconsulting/pyubx2/blob/master/CONTRIBUTING.md)).
- [ ] I have performed a self-review of my own code.
- [ ] (*if appropriate*) I have cited my u-blox documentation source(s).
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have made corresponding changes to the documentation.
- [ ] (*if appropriate*) I have added test cases to the `tests/test_*.py` unittest suite to maintain >= 99% code coverage.
- [ ] I have tested my code against the full `tests/test_*.py` unittest suite.
- [ ] My changes generate no new warnings.
- [ ] Any dependent changes have been merged and published in downstream modules.
- [ ] I have [signed](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits) my commits.
- [ ] I understand and acknowledge that the code will be published under a BSD 3-Clause license.
