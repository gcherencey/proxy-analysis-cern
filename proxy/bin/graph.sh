#!/bin/bash

args=("$@")

db=${args[0]}
max_Time=${args[1]}
i=0

if [ ${#args[*]} != 2 ]
then
	echo "
		 Usage: graph.sh db max_Time

       		     db -> the name of your database file
       		     max_time -> the maximum time you want your object into the proxy cache
		     "
else

	##################################################
	# Calculate the ratio global and for each center

	if [ ! -e ALL_ratioglobal_${db}_${max_Time}.csv ]
	then
		for i in $(seq 10 10 450)
		do 
			analysis ${db} 0 ${i} ${max_Time} ratioglobal_${db}_${max_Time}.csv
		done
	fi

	#################################################################
	# Calculate the hit ratio per max_Time for a ratio of 70,210,270

	if [ ! -e ALL_hitratio_per_max_Time_${db}_70.csv ]
	then
		for i in $(seq 30 30 600)
		do 
			analysis ${db} 0 70 ${i} hitratio_per_max_Time_${db}_70.csv
			analysis ${db} 0 210 ${i} hitratio_per_max_Time_${db}_210.csv
			analysis ${db} 0 270 ${i} hitratio_per_max_Time_${db}_270.csv
		done
	fi

	############################
	# Create the plot Delta.png
	if [ -e "ALL_${db}_Delta.csv" ];then

		gnuplot -persist << GPLOT
	
		set datafile separator ','

		set title "Time between two requests\n batadase -> ${db} ratio -> 250"
		set xlabel 'Sites'
		set ylabel 'Minutes'
		set zlabel 'Number of requests' rotate by 90
		set yrange [0:200]
				
		set ticslevel 0.0
		set grid

		splot "ALL_${db}_Delta.csv" u 1:2:3 with boxes title "Global","LCG.NIKHEF.nl,LCG.SARA.nl_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.NIKHEF.nl,LCG.SARA.nl", "LCG.IN2P3.fr,LCG.IN2P3-T2.fr_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.IN2P3.fr,LCG.IN2P3-T2.fr","LCG.PIC.es_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.PIC.es", "LCG.RAL.uk_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.RAL.uk", "LCG.CNAF.it,LCG.CNAF-T2.it_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.CNAF.it,LCG.CNAF-T2.it", "LCG.GRIDKA.de_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.GRIDKA.de", "LCG.CERN.ch_${db}_Delta.csv" u 1:2:3 with boxes title "LCG.CERN.ch"

		set term png
		set out '${db}_Delta.png'

		replot

		quit
	

GPLOT
	
	fi

	############################
	# Create the plot RequestPerHour.png

	if [ -e "ALL_${db}_RequestPerhour.csv" ];then

		gnuplot -persist << GPLOT
	
		set datafile separator ','

		set title "Number of requests per hour\n batadase -> ${db} ratio -> 250"
		set xlabel 'Sites'
		set ylabel 'Hours'
		set zlabel 'Number of requests' rotate by 90

		set ticslevel 0.0
		set grid

		splot "ALL_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "Global","LCG.NIKHEF.nl,LCG.SARA.nl_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.NIKHEF.nl,LCG.SARA.nl", "LCG.IN2P3.fr,LCG.IN2P3-T2.fr_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.IN2P3.fr,LCG.IN2P3-T2.fr","LCG.PIC.es_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.PIC.es", "LCG.RAL.uk_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.RAL.uk", "LCG.CNAF.it,LCG.CNAF-T2.it_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.CNAF.it,LCG.CNAF-T2.it", "LCG.GRIDKA.de_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.GRIDKA.de", "LCG.CERN.ch_${db}_RequestPerhour.csv" u 1:2:3 with boxes title "LCG.CERN.ch"
		
		set term png
		set out '${db}_RequestPerHour.png'

		replot

		quit

GPLOT
	
	fi

	##################################
	# Create the plot graph_per_ratio

	if [ -e "ALL_ratioglobal_${db}_${max_Time}.csv" ];then
	
		gnuplot -persist << GPLOT

		set datafile separator ','

		set title "Global graph : evolution of hit ratio vs. ratio (range/time_To_Add)\nParameter : db -> ${db}, max_Time -> ${max_Time}"
		set xlabel 'Ratio (range/time_To_Add)'
		set ylabel 'Hit Ratio (%)'
		set xrange [0:450]
		set yrange [0:100]
		set key right bottom
		set grid

		plot "ALL_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "Global","LCG.NIKHEF.nl,LCG.SARA.nl_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.NIKHEF.nl,LCG.SARA.nl","LCG.IN2P3.fr,LCG.IN2P3-T2.fr_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.IN2P3.fr,LCG.IN2P3-T2.fr","LCG.PIC.es_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.PIC.es","LCG.RAL.uk_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.RAL.uk","LCG.CNAF.it,LCG.CNAF-T2.it_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.CNAF.it,LCG.CNAF-T2.it","LCG.GRIDKA.de_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.GRIDKA.de", "LCG.CERN.ch_ratioglobal_${db}_${max_Time}.csv" using 1:3 w l title "LCG.CERN.ch"

		set term png
		set out 'graph_per_ratio_${db}_${max_Time}.png'

		replot

		quit

GPLOT

	fi


	#####################################
	# Create the plot graph_per_max_Time

	if [ -e "ALL_hitratio_per_max_Time_${db}_70.csv" ];then
	
		gnuplot -persist << GPLOT

		set datafile separator ','

		set title "Global graph : evolution of hit ratio vs. self.max\nParameter : db -> ${db}"
		set xlabel 'self.max (min.)'
		set ylabel 'Hit Ratio (%)'
		set xrange [0:600]
		set yrange [0:100]
		set key right bottom
		set grid

		plot "ALL_hitratio_per_max_Time_${db}_70.csv" using 2:3 w l title "ratio : 70","ALL_hitratio_per_max_Time_${db}_210.csv" using 2:3 w l title "ratio : 210","ALL_hitratio_per_max_Time_${db}_270.csv" using 2:3 w l title "ratio : 270"

		set term png
		set out 'graph_per_max_Time_${db}.png'

		replot

		quit

GPLOT

	fi

fi
