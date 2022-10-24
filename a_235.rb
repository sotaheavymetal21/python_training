a = gets.chomp.split("")
puts a
aa = []
bb = []
cc = []
aa << a[0] + a[1] + a[2]
bb << a[1] + a[2] + a[0]
cc << a[2] + a[0] + a[1]
puts aa[0].to_i + bb[0].to_i + cc[0].to_i
