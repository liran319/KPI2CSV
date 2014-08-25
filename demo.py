import re

s = """
    Aug 21 15:13:37 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>close end  = 1408605217205.926025 ms, close using time: 1.361084 
    Aug 21 15:44:39 Viviande-mini2 Ericsson_SamplePlayer[2226] <Warning>: >>>>>>>>>>run end  = 1408607079531.018066 ms run using time = 1.402100 
    Aug 21 15:44:40 Viviande-mini2 Ericsson_SamplePlayer[2226] <Warning>: >>>>>>>>>>buffer using time = 1167.613983 ms 
    Aug 21 15:44:48 Viviande-mini2 Ericsson_SamplePlayer[2226] <Warning>: >>>>>>>>>>buffer using time = 7568.030953 ms 
    Aug 21 15:44:50 Viviande-mini2 Ericsson_SamplePlayer[2226] <Warning>: >>>>>>>>>>stop end  = 1408607090390.548828 ms, stop using time: 1166.609863 
    """

p1 = "Init using time.{2}(\d*) ms,"
p2 = "Open using time.{2}(\d*) ms,"
p3 = "\w{3} \d{2} \d{2}:\d{2}:\d{2}.{100}run using time.{3}(\d*\.\d*)"
p4 = "\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}\s.{101}stop using time:\s(\d*\.\d*)"

result1 = re.findall(p4, s)
result2 = re.findall(p3, s)

print result1
print result2
