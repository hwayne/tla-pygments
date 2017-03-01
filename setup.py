from setuptools import setup, find_packages
 
setup (
  name='tlalexer',
  packages=find_packages(),
  entry_points =
  """
  [pygments.lexers]
  tlalexer = tlalexer.lexer:TlaLexer
  """,
)
