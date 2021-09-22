npm install uglify-js -g
npm install uglifycss -g

# Minify the js files
$files = Get-ChildItem ./ -recurse -force -include *.js | where-object{$_.fullname -notlike '*node_modules*'}  | where-object{$_.fullname -notlike '*min*'}
foreach($file in $files){
   uglifyjs $file.FullName -o $file.FullName.Replace('.js', '.min.js')
 }

# Minify the css
$files = Get-ChildItem ./ -recurse -force -include *.css | where-object{$_.fullname -notlike '*node_modules*'}  | where-object{$_.fullname -notlike '*min*'}
foreach($file in $files){
   uglifycss $file.FullName > $file.FullName.Replace('.css', '.min.css')
}

# Minify the html
$files = Get-ChildItem ./ -recurse -force -include *.html | where-object{$_.fullname -notlike '*node_modules*'}  | where-object{$_.fullname -notlike '*min*'}
foreach($file in $files){
    java -jar build/htmlcompressor-1.5.3.jar $file.FullName > $file.FullName.Replace('.html', '.min.html')
}
