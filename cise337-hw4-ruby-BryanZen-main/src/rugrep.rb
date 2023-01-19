#!/usr/bin/env ruby
args = ARGF.argv
class MyError < StandardError
end

def valid_regex?(str)
  Regexp.new(str)
  true
rescue
  false
end

def parseArgs(args)
  retStr = ""
  optionList = [] #list of options given
  patternList = [] #list of patterns given "pattern"
  fileList = [] #list of filenames given
  fileMaster = [] #list of lists of each line in a valid file without the new line
  validFiles = [] #list of valid filenames
  validPatterns = [] #list of valid patterns: pattern (no quotes)
  begin
    foundPattern = false
    lastIsPattern = false
    validOptions = %w[-v --invert-match -c --count -l --files-with-matches -L --files-without-match -o --only-matching -F --fixed-strings]
    args.each { |arg|
      if args.length() < 2 #less than 2 arguments
        raise MyError
      elsif arg[0] == "\"" and arg[-1] == "\"" #patterns are not contiguously placed, i.e., if a list of patterns are provided as arguments they must occur one after the other in the arguments
        if foundPattern == true and lastIsPattern == false
          raise MyError
        end
        patternList.append(arg)
        foundPattern = true
        lastIsPattern = true
      elsif arg[0] == "-" #invalid option names, i.e., option names not listed above
        validOptions.each {|option|
          if not arg == option
            raise MyError
          end
        }
        optionList.append(arg)
        lastIsPattern = false
      else
        fileList.append(arg) #file found after finding options and patterns
        lastIsPattern = false
      end
    }
    if optionList.length() == 2 #invalid 2 option combinations, i.e., option combinations not listed above
      if optionList.include?("-c") or optionList.include?("--count")
        if not optionList.include?("-v") or optionList.include?("--invert-match") or optionList.include?("-o") or optionList.include?("--only-matching") or optionList.include?("-F") or optionList.include?("--fixed-strings")
          raise MyError
        end
      end
      if optionList.include?("-F") or optionList.include?("--fixed-strings")
        if not optionList.include?("-o") or optionList.include?("--only-matching") or optionList.include?("-v") or optionList.include?("--invert-match")
          raise MyError
        end
      end
      if optionList.include?("-v") or optionList.include?("--invert-match")
        if not optionList.include?("A_NUM") or optionList.include?("--after-context=num") or optionList.include?("-B_NUM") or optionList.include?("--before-context=num") or optionList.include?("-C_NUM") or optionList.include?("--context=num")
          raise MyError
        end
      end
    elsif optionList.length() == 3 #invalid 3 option combinations, i.e., option combinations not listed above
      if not (optionList.include?("-F") or optionList.include?("--fixed-strings")) and (optionList.include?("-v") or optionList.include?("--invert-match")) and (optionList.include?("-c") or optionList.include?("--count"))
        raise MyError
      end
    end
    if patternList.length() == 0 or optionList.length() > 3 #no patterns are provided as arguments
      raise MyError
    end
    rescue MyError => e #extends standard error
      puts "USAGE: ruby rugrep.rb "
      exit
  end
  if fileList.length() == 0 #no files to be read
    raise IOError, "Error: could not read file"
  end
  fileList.each do |fileName|
    begin
      file = File.open(fileName)
      fileData = file.readlines.map(&:chomp)
      fileMaster.append(fileData)
      validFiles.append(fileName)
    end
    rescue SystemCallError => e
      puts "Error: could not read file path/to/" + fileName
  end
  if validFiles.length() == 0 #no valid files to be read
    raise IOError, "Error: could not read file"
  end
  patternList.each do |pattern| #checks if patterns are valid ruby regular expressions,
    p = pattern[1..-2]
    if valid_regex?(p)
      validPatterns.append(p)
    else
      puts "Error: cannot parse regex"
    end
  end
  #call optional argument functions
  if optionList.length() == 0
    retStr += match(patternList, fileMaster, validFiles)
  end
  if optionList.include?("-v") or optionList.include?("--invert-match")
    if optionList.length() == 1
      retStr += invertMatch(patternList, fileMaster, validFiles)
    end
  end
  if optionList.include?("-c") or optionList.include?("--count")
    combo = []
    if optionList.length() == 1
      retStr += count(combo, patternList, fileMaster, validFiles)
    end
    if optionList.length() == 2
      if optionList.include?("-v") or optionList.include?("--invert-match")
        combo.append("-v")
        retStr += count(combo, patternList, fileMaster, validFiles)
      end
    end
  end
  if optionList.include?("-l") or optionList.include?("--files-with-matches")
    if optionList.length() == 1
      retStr += filesWithMatches(patternList, fileMaster, validFiles)
    end
  end
  if optionList.include?("-L") or optionList.include?("--files-without-match")
    if optionList.length() == 1
      retStr += filesWithoutMatches(patternList, fileMaster, validFiles)
    end
  end
  if optionList.include?("-o") or optionList.include?("--only-matching")
    combo = []
    if optionList.length() == 1
      retStr += onlyMatching(patternList, fileMaster, validFiles)
    end
    if optionList.length() == 2
      if optionList.include?("-c") or optionList.include?("--count")
        retStr += count(combo, patternList, fileMaster, validFiles)
      end
    end
  end
  if optionList.include?("-F") or optionList.include?("--fixed-strings")
    combo = []
    if optionList.length() == 1
      retStr += fixedStrings(combo, patternList, fileMaster, validFiles)
    end
    if optionList.length() == 2
      if optionList.include?("-c") or optionList.include?("--count")
        combo.append("-c")
        retStr += fixedStrings(combo, patternList, fileMaster, validFiles)
      end
      if optionList.include?("-o") or optionList.include?("--only-matching")
        combo.append("-o")
        retStr += fixedStrings(combo, patternList, fileMaster, validFiles)
      end
      if optionList.include?("-v") or optionList.include?("--invert-match")
        combo.append("-v")
        retStr += fixedStrings(combo, patternList, fileMaster, validFiles)
      end
    end
    if optionList.length() == 3
      if (optionList.include?("-v") or optionList.include?("--invert-match")) and (optionList.include?("-c") or optionList.include?("--count"))
        combo.append("-v")
        combo.append("-c")
        retStr += fixedStrings(combo, patternList, fileMaster, validFiles)
      end
    end
  end
  if optionList.include?("-A_NUM") or optionList.include?("--after-context=num")
    combo = []
    if optionList.length() == 1
      retStr += afterContext(combo, patternList, fileMaster, validFiles)
    end
    if optionList.length() == 2
      if optionList.include?("-v") or optionList.include?("--invert-match")
        combo.append(-v)
        retStr += afterContext(combo, patternList, fileMaster, validFiles)
      end
    end
  end
  if optionList.include?("-B_NUM") or optionList.include?("--before-context=num")
    combo = []
    if optionList.length() == 1
      retStr += beforeContext(combo, patternList, fileMaster, validFiles)
    end
    if optionList.length() == 2
      if optionList.include?("-v") or optionList.include?("--invert-match")
        combo.append(-v)
        retStr += beforeContext(combo, patternList, fileMaster, validFiles)
      end
    end
  end
  if optionList.include?("-C_NUM") or optionList.include?("--context=num")
    if optionList.length() == 1

    end
    if optionList.length() == 2
      if optionList.include?("-v") or optionList.include?("--invert-match")

      end
    end
  end
  return retStr
end

def match(patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if line.match(p)
          if validFiles.length() == 1
            retStr += line + "\n"
          else
            retStr += validFiles[fileNumber] + ": " + line + "\n"
          end
        end
      }
    }
    fileNumber += 1
  end
  return retStr
end
def invertMatch(patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if not line.match(p)
          if validFiles.length() == 1
            retStr += line + "\n"
          else
            retStr += validFiles[fileNumber] + ": " + line + "\n"
          end
        end
      }
    }
    fileNumber += 1
  end
  return retStr
end
def count(combo, patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    fileMatch = 0
    fileNoMatch = 0
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if line.match(p)
          fileMatch += 1
        else
          fileNoMatch += 1
        end
      }
    }
    if combo.length() == 0
      if validFiles.length() == 0
        retStr += fileMatch.to_s + "\n"
      else
        retStr += validFiles[fileNumber] + ": " + fileMatch.to_s + "\n"
      end
    end
    if combo.length() == 1
      if validFiles.length() == 0
        retStr += fileNoMatch.to_s + "\n"
      else
        retStr += validFiles[fileNumber] + ": " + fileNoMatch.to_s + "\n"
      end
    end
    fileNumber += 1
  end
  return retStr
end
def filesWithMatches(patternList, fileMaster, validFiles)
  retStr = ""
  boolFiles = Array.new(validFiles.length(), false)
  fileNumber = 0
  fileMaster.each do |file|
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if line.match(p)
          boolFiles[fileNumber] = true
        end
      }
    }
    fileNumber += 1
  end
  boolIndex = 0
  boolFiles.each do |bool|
    if bool
      retStr += validFiles[boolIndex] + "\n"
    end
    boolIndex += 1
  end
  return retStr
end
def filesWithoutMatches(patternList, fileMaster, validFiles)
  retStr = ""
  boolFiles = Array.new(validFiles.length(), false)
  fileNumber = 0
  fileMaster.each do |file|
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if not line.match(p)
          boolFiles[fileNumber] = true
        end
      }
    }
    fileNumber += 1
  end
  boolIndex = 0
  boolFiles.each do |bool|
    if bool
      retStr += validFiles[boolIndex] + "\n"
    end
    boolIndex += 1
  end
  return retStr
end
def onlyMatching(patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        found = line.scan(p) #list of found matches in a line
        found.each {|match|
          if validFiles.length() == 0
            retStr += match + "\n"
          else
            retStr += validFiles[fileNumber] + ": " + match + "\n"
          end
        }
      }
    }
    fileNumber += 1
  end
  return retStr
end
def fixedStrings(combo, patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    fileMatch = 0
    fileNoMatch = 0
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        fixedP = p.to_s
        if line.include?(fixedP)
          if combo.length() == 0
            if validFiles.length() == 1
              retStr += line + "\n"
            else
              retStr += validFiles[fileNumber] + ": " + line + "\n"
            end
          end
          fileMatch += 1
        end
        if not line.include?(fixedP)
          if combo.length() == 1
            if combo.includes?("-v")
              if validFiles.length() == 1
                retStr += line + "\n"
              else
                retStr += validFiles[fileNumber] + ": " + line + "\n"
              end
            end
            fileNoMatch += 1
          end
        end
        found = line.scan(fixedP) #list of found matches in a line
        if combo.length() == 1
          if combo.includes?("-o")
            found.each {|match|
              if validFiles.length() == 0
                retStr += match + "\n"
              else
                retStr += validFiles[fileNumber] + ": " + match + "\n"
              end
            }
          end
        end
      }
    }
    if combo.length() == 1
      if combo.includes?("-c")
        if validFiles.length() == 0
          retStr += fileMatch.to_s + "\n"
        else
          retStr += validFiles[fileNumber] + ": " + fileMatch.to_s + "\n"
        end
      end
    end
    if combo.length() == 2
      if validFiles.length() == 0
        retStr += fileNoMatch.to_s + "\n"
      else
        retStr += validFiles[fileNumber] + ": " + fileNoMatch.to_s + "\n"
      end
    end
    fileNumber += 1
  end
  return retStr
end
def afterContext(combo, patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    lineNum = 0
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if combo.length() == 0
          if line.match(p)
            if validFiles.length() == 1
              retStr += line + "\n" + (file.length() - lineNum - 1).to_s + "\n"
            else
              retStr += validFiles[fileNumber] + ": " + line + "\n" + validFiles[fileNumber] + ": " + (file.length() - lineNum - 1).to_s + "\n"
            end
          end
        end
        if combo.length() == 1
          if not line.match(p)
            if validFiles.length() == 1
              retStr += line + "\n" + (file.length() - lineNum - 1).to_s + "\n"
            else
              retStr += validFiles[fileNumber] + ": " + line + "\n" + validFiles[fileNumber] + ": " + (file.length() - lineNum - 1).to_s + "\n"
            end
          end
        end
      }
      lineNum += 1
    }
    fileNumber += 1
  end
  return retStr
end
def beforeContext(combo, patternList, fileMaster, validFiles)
  retStr = ""
  fileNumber = 0
  fileMaster.each do |file|
    lineNum = 0
    file.each {|line|
      patternList.each{|pattern|
        p = Regexp.new(pattern)
        if combo.length() == 0
          if line.match(p)
            if validFiles.length() == 1
              retStr += line + "\n" + (file.length() - lineNum - 1).to_s + "\n"
            else
              retStr += validFiles[fileNumber] + ": " + line + "\n" + validFiles[fileNumber] + ": " + lineNum.to_s + "\n"
            end
          end
        end
        if combo.length() == 1
          if not line.match(p)
            if validFiles.length() == 1
              retStr += line + "\n" + (file.length() - lineNum - 1).to_s + "\n"
            else
              retStr += validFiles[fileNumber] + ": " + line + "\n" + validFiles[fileNumber] + ": " + lineNum.to_s + "\n"
            end
          end
        end
      }
      lineNum += 1
    }
    fileNumber += 1
  end
  return retStr
end
def context(combo, patternList, fileMaster, validFiles)

end

puts parseArgs(args)
