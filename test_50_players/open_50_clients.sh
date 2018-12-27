for k in $(seq 1 10) ; do
	firefox -new-window 'http://127.0.0.1:5000'
	sleep 1
	echo $k
done
echo 'pages ouvertes'
