require 'simplecov'
SimpleCov.start
require_relative File.join("..", "src", "rugrep")
require 'test/unit'
require 'test/unit/assertions'
require 'set'
require_relative "../rugrep.rb"

class MyTest < Test::Unit::TestCase
  def test_input_valid
    args = ["-v", "\"Socrates\"", "\"Plato\"", "../input.txt"]
    assert(parseArgs(args))

  end
end
