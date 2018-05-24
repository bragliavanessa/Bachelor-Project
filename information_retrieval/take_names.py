# coding=utf-8

# Lets use a regular expression to extract members' names
# from the crawled html pages
import re
import os
import json
import unicodedata


'''###########
    UNI map
 ############'''
uni_map = {
    "TODELETE":["SENAI CIMATEC","SPACI","STIS","Scientific Computing in Life Sciences","Symetrics","Principal Consultant","PUB - LMN","PQI Consulting","Consultant","Cluster File Systems","CREATE-AV","CORIA","CINVESTAV","CERFACS","Transfer Solutions","Technology","TIT/JST","www.charlesperry.com","Environment and Climate Change","Retired from Commissariat a l'Energie Atomique (CEA)","Research","ReproducibleResearch.org","Numerica",
                 "Ireq","Intelligent Light","Independent Consultant","ITAM","Mechanics","LaBRI","Gurobi GmbH","OFFIS","OPTSEG - Optimal Safety Engineering","Freelance Computational Scientist"],
    "Amazon":["Amazon.com"],
 "FEEC":["FEEC/UNICAMP"],
 "ONERA":["ONERA-CERT"],
 "Indian Institute of Technology":["Indian Institute of Technology (Banaras Hindu University)","Indian Institute of Technology Bombay","Indian Institute of Technology Guwahati","Indian Institute of Technology Kharagpur","Indian Institute of Technology Madras","Indian Institute of Technology Mandi","Indian Institute of Technology Roorkee","Indian Institute of Technology, Delhi","Indian Institute of Technology, Guwahati","Indian Institute of Technology, Kanpur","Indian Institute of Technology-Bombay"],
 "Indiana University":["Indiana University","University of Indiana","Indiana University - Purdue University Indianapolis","Indiana University Bloomington","Indiana University and The Technion","Indiana University-Purdue University Columbus"],
 "Imperial College":["Imperial College London","Imperial College of London","Imperial College, London"],
 "University of Milano":["University of Milano","University of Milan","Milano University","Universita di Milano","Universita degli Studi di Milano","Universit&agrave; degli Studi di Milano"],
 "Moscow State University":["Moscow State University of Railway Engineering"],
 "Free University of Berlin":["Free University of Berlin","Freie Universitaet Berlin","Freie Universität Berlin","University of Berlin"],
 "Facebook":["Facebook AI Research"],
 "IASI":["Istituto di Analisi dei Sistemi e Informatica IASI Consiglio Nazionale delle Ricerche CNR"],
 "Lawrence Livermore National Laboratory":["Lawrence Livermore National Laboratory and University of Utah"],
 "Lawrence Berkeley National Laboratory":["Lawrence Berkeley National Laboratory and Stanford University","Lawrence Berkeley National Laboratory and University of California Berkeley","Lawrence Berkeley National Laboratory and University of Oregon",""],
 "GERAD":["GERAD & Polytechnique Montreal"],
 "Hebrew University":["Hebrew University","Hebrew University of Jerusalem","The Hebrew University"],
 "LIFL":["LIFL","LIFL and CNRS"],
 "INSA Rouen":["INSA Rouen","INSA de Rouen","National Institute for Applied Sciences, Rouen"],
 "IRISA":["IRISA","IRISA-Inria"],
 "IRSN":["IRSN and UNIBE"],
 "Mitsubishi Research Institute, Inc.":["Mitsubishi Electric Research Laboratories","Mitsubishi Research Institute, Inc."],
 "Michigan Technological University":["Michigan Technological University","Michigan Tech Research Institute"],
 "Microsoft Corporation":["Microsoft","Microsoft Corporation","Microsoft Research","Microsoft Research Cambridge","Microsoft Research New England","Microsoft Research Silicon Valley","Microsoft Research and Technion - Israel Institute of Technology","Microsoft Research-Inria Joint Centre"],
 "Miami University":["Miami University","University of Miami","Miami University Hamilton","Miami University and University of Kansas"],
 "Mentor Graphics Corporation":["Mentor Graphics Corporation","Mentor Graphics"],
 "Leibniz University Hannover":["Leibniz University Hannover","Leibniz Universität Hannover","University of Hannover"],
 "Laboratoire Jacques-Louis Lions":["Laboratoire Jacques-Louis Lions and Université Pierre et Marie Curie - Paris 6","Laboratoire Jacques-Louis Lions"],
 "Florida A&M University":["Florida A & M University"],
 "FORTH-ICS":["FORTH-ICS and University of Crete"],
 "Heriot-Watt University":["Heriot-Watt University, Edinburgh"],
 "Heidelberg Institute for Theoretical Studies":["Heidelberg Institute for Theoretical Studies","Heidelberg Institute for Theoretical Studies and Karlsruhe Institute of Technology"],
 "General Electric Global Research Center":["General Electric Global Research Center","General Electric"],
 "Swedish National Defence Research Institute":["FOI - The Swedish Defence Research Agency","Swedish Defense Research Agency"],
 "University of Namur":["Facultés Universitaires Notre-Dame de la Paix","Universite Notre Dame de la Paix and University of Namur","University of Namur","University of Notre Dame"],
 "Adam Mickiewicz University":["A.Mickiewicz University","Adam Mickiewicz University"],
 "Baruch College":["Baruch College, CUNY"],
 "G-SCOP":["G-SCOP, Grenoble"],
 "BT Research":["BT Networks Research Centre"],
 "Friedrich Schiller University Jena":["University of Jena","Friedrich-Schiller-Universität Jena","Friedrich Schiller Universität Jena"],
 "BITS":["BITS Pilani"],
 "IBM":["IBM","IBM Almaden Research Center","IBM Corporation","IBM Deutschland Research & Development GmbH","IBM Haifa Research Lab","IBM Research","IBM Research - Tokyo","IBM Research Tel-Aviv","IBM Research-Zurich","IBM Software Group","IBM T.J. Watson Research Center","IIT Roorkee"],
 "Oak Ridge National Laboratory":["Oak Ridge National Laboratory and University of Notre Dame"],
 "National Cancer Institute":["National Cancer Institute","National Cancer Institute and National Institutes of Health"],
 "T-Systems":["T-Systems International"],
 "Criteo":["CRITEO"],
 "Numerical Algorithms Group":["Numerical Algorithms Group Ltd"],
 "Northrop Grumman Corporation":["Northrop Grumman Corporation","Northrop Grumman Corp."],
 "NTNU":["Norwegian University of Science and Technology","Norwegian University of Science and Technology and University of Vienna","University of Natural Resources and Applied Life Sciences"],
 "North Carolina Agricultural and Technical State University":["North Carolina Agricultural and Technical State University","North Carolina A&T State University","North Carolina State University"],
 "National Research Nuclear University":["National Research Nuclear University","National Research Nuclear University MEPhI"],
 "North Fluminense State University":["North Fluminense State University Darcy Ribeiro","North Fluminense State University"],
 "SISSA":["SISSA/Trieste","SISSA-ISAS International School for Advanced Studies","International School for Advanced Studies, Trieste"],
 "NEC Corporation":["NEC Europe Ltd","NEC Informatec Systems LTD","NEC Soft, Ltd.","NEC Solution Innovators, Ltd."],
 "BRGM":["BRGM","BRGM/STI"],
 "National University of Singapore":["National University of Singapore","National University of Singapore and IHPC","NTU Singapore","Nanyang Technical University","Nanyang Technological University"],
 "NASA":["NASA","NASA Ames Research Center","NASA Goddard Institute for Space Studies","NASA Goddard Space Flight Center","NASA Langley Research Center","NASA/GSFC Global Modeling and Assimilation Office, SSAI Inc."],
 "SINTEF":["SINTEF","SINTEF Energy Research"],
 "NITK Surathkal":["NIT Surathkal"],
 "IDC Herzliya":["Interdisciplinary Center Herzliya"],
 "National Academy of Science":["National Academy of Science","National Academy of Sciences"],
 "NSWC Panama City":["NSWC PC"],
 "SAMSI":["SAMSI and University of North Carolina at Chapel Hill"],
 "SIAM":["SIAM","SIAM Activity Group on Geometric Design"],
 "QuantM Ltd":["Quantm Ltd."],
 "Queen's University":["Queen's University","Queen's University, Belfast"],
 "Pusan National University":["Pusan National University, Busan (Pusan)"],
 "Princeton University":["Princeton University","Princeton University and Bordeaux 1 University","Princeton University and INTECH LLC","Princeton University and Microsoft Research"],
 "Institute Pprime":["PPRIME"],
 "Preferred Networks, Inc.":["Preferred Networks"],
 "IMPA Instituto Nacional de Matemática Pura e Aplicada":["IMPA, Rio de Janeiro"],
 "IMECC UniCamp":["IMECC - UniCamp","IMEC","IMECC-UNICAMP","DMA-IMECC-UNICAMP"],
 "IIT":["IIT Bombay","IIT Delhi","IIT Kanpur","IIT Roorkee"],
 "ICREA":["ICREA and Universitat Politècnica de Catalunya"],
 "IFP Energies nouvelles":["IFP Energies nouvelles","IFP","IFPEN"],
 "Safran Tech":["Safran Tech","Safran, Research & Technology Center"],
 "Saint Joseph's University":["Saint Joseph's University","Saint Joseph University"],
 "Sandia National Laboratories":["Sandia National Laboratories","Sandia National Laboratory"],
 "Schlumberger":["Schlumberger Brazil Research and Geoengineering Center","Schlumberger Cambridge Research","Schlumberger Moscow Research","Schlumberger Riboud Product Center","Schlumberger-Doll Research"],
 "Science and Technology Facilities Council":["Science and Technology Facilities Council","Science & Technology Facilities Council"],
 "Pontifical Catholic University of Rio de Janeiro":["Pontificia Universidade Catolica Do Rio de Janeiro"],
 "Politecnico di Milano":["Polytechnic Institute Milano"],
 "Pohang University of Science and Technology":["Pohang Accelerator Lab, POSTECH"],
 "Palantir Technologies":["Palantir"],
 "Cray, Inc.":["Cray Inc.","Cray Inc. and University of Minnesota"],
 "Colorado State University":["Colorado State University","Colorado State University and Naval Postgraduate School"],
 "COPPE, Universidade Federal do Rio e Janeiro":["COPPE/Universidade Federal do Rio e Janeiro"],
 "CERMICS":["CERMICS","CERMICS ENPC"],
 "ICAR CNR":["ICAR-CNR"],
 "LRZ":["LRZ: Leibniz Supercomputing Centre"],
 "Fraunhofer-Gesellschaft Institute":["Fraunhofer Institute for Industrial Mathematics","Fraunhofer Institute for Physical Measurement Techniques","Fraunhofer MEVIS","Fraunhofer-Chalmers Research Centre","Fraunhofer-Institut für Algorithmen und Wissenschaftliches Rechnen","Fraunhofer-Institut für Informations- und Datenverarbeitung","Fraunhofer-Institut für Techno- und Wirtschaftsmathematik"],
 "Telecom":["France Telecom Research and Development"],
 "U.S. Geological Survey":["U. S. Geological Survey"],
 "U.S. Naval Academy":["U. S. Naval Academy","United States Naval Academy","US Naval Research Laboratory","US Naval Academy"],
 "CNIT":["Consorzio Nazionale Interuniversitario per le Telecomunicazioni (CNIT)"],
 "CNRS":["LIMSI-CNRS","CNRS & Ecole Polytechnique","CNRS & Universite de Marseille","CNRS - Ecole Normale Superieure","CNRS / UPMC","CNRS and ENS Lyon","CNRS and Ecole des Mines de St Etienne","CNRS and Grenoble University","CNRS and Inria Sophia-Antipolis","CNRS and UPMC","CNRS and Université Pierre et Marie Curie","CNRS, GREYC Laboratory","CNRS, Université Paris-Saclay","CNRS, Université de Rennes 1","CNRS-ENS Paris","CNRS-IRIT","CNRS/LIFL","CNRS/LIFL and Inria"],
 "TIFR Centre":["TIFR Centre, Bangalore"],
 "Istituto per le Applicazioni del Calcolo Mauro Picone":["Istituto per le Applicazioni del Calcolo \"Mauro Picone","Istituto per le Applicazioni del Calcolo \"Mauro Picone\""],
 "CNR":["CNR","Istituto di Analisi dei Sistemi ed Informatica del CNR, Rome","Istituto di Calcolo e Reti ad Alte Prestazioni - CNR","Istituto di Matematica Applicata e Tecnologie Informatiche-CNR","CNR-INSEAN","CNR-INSEAN, National Research Council-Marine Technology Research Institute"],
 "Hungarian Academy of Science":["Academy of Science, Budapest"],
 "AMPL":["AMPL Optimization"],
 "U.S. Army":["US Army ARL-ARDEC","US Army Cold Regions Research and Engineering Lab (CRREL)","US Army Corps of Engineers","US Army Engineer Research and Development Center","United States Army Corps of Engineers","U.S. Army Engineer Research and Development Center","U.S. Army Research Development Engineering Command"],
 "Technical University Eindhoven":["Technische Universiteit Eindhoven","TU Eindhoven and TU Delft","TU Eindhoven","TU Eindhoven","TU Eindhoven and TU Delft"],
 "BTS":["Bayer Technology Services GmbH, Leverkusen"],
 "Technical University Munchen":["TU München","Technische Universität München"],
 "ASA":["Advanced Solutions Accelerator"],
 "Technical University Braunschweig":["Technische Universität Braunschweig","Technische Universitaet Braunschweig","Technical University Braunschweig","TU Braunschweig"],
 "Technical University Berlin":["Technische Universität, Berlin","Technische Universität Berlin","Technische Universitat Berlin","Technical University of Berlin","Technische Universitaet Berlin","Technical University Berlin","TU Berlin"],
 "Technical University Darmstadt":["Technische Universität Darmstadt","Technische Universitaet Darmstadt","Technical University Darmstadt","TU Darmstadt"],
 "Air Force Research Laboratory":["ERC Inc. and Air Force Research Laboratory","Air Force Research Laboratory","Air Force Office of Scientific Research","Air Force Institute of Technology","Air Force Academy"],
 "Agrosphere Institute":["Agrosphere Institute","Agrosphere Research Center Jülich"],
 "Technical University Ostrava":["TU Ostrava"],
 "Technical University Cartagena":["Technical University of Cartagena"],
 "Technical University Chemnitz":["Technical University of Chemnitz"],
 "Technical University Cluj-Napoca":["Technical University of Cluj-Napoca"],
 "Technical University Crete":["Technical University of Crete"],
 "Technical University Denmark":["Technical University of Denmark"],
 "Technical University Liberec":["Technical University of Liberec"],
 "Technical University Lisbon":["Technical University of Lisbon"],
 "Technical University Ilmenau":["Technische Universität Ilmenau"],
 "University of Kaiserslautern":["University of Kaiserslautern","Technical University Kaiserslautern","Technische Universität Kaiserslautern"],
 "Technical University Graz":["Technical University Graz","Technische Universität, Graz","Graz University of Technology"],
 "Technical University Hamburg":["Technische Universität Hamburg-Harburg","Hamburg University of Technology"],
 "AGH UST":["AGH University of Science and Technology"],
 "Technical University Delft":["Technical University of Delft","Technische Universität Delft","Technical University of Delft","TU Delft"],
 "Technical University Muenchen":["Technische Universitaet Muenchen"],
 "Technical University Munich":["TU Munich","Technical University of Munich"],
 "Technical University Dresden":["Technische Universität Dresden","TU Dresden","Technische Universitaet Dresden"],
 "Technical University Dortmund":["Technische Universität Dortmund","TU Dortmund","Universit&auml;t Dortmund","University of Dortmund"],
 "Technical University Chemnitz":["TU Chemnitz","Technische Universitat Chemnitz"],
 "Technical University Bergakademie Freiberg":["Technische Universität Bergakademie Freiberg","TU Bergakademie Freiberg","Technische Universitaet Bergakademie Freiberg"],
 "Aimdyn, Inc.":["AIMdyn, Inc."],
 "Technicolor":["Technicolor - Inria", "Technicolor R&D France"],
 "Technion IIT":["Technion","Technion - Israel Institute of Technology","Technion IIT, Haifa","Technion Israel Institute of Technology","IIT Bombay","IIT Kanpur"],
 "USI":["USI","University of Lugano","Università della Svizzera italiana"],
 "Universite of Neuchatel":["Universite de Neuchatel","University of Neuchatel"],
 "University of Basel":["University of Basel","Universität Basel"],
 "University of Bern":["University of Bern","University of Berne"],
 "University of Geneva":["University of Geneva","Université de Genève"],
 "University of Genova":["University of Genoa","University of Genova"],
 "UNIL":["University of Lausanne"],
 "Airbus Operation SAS":["Airbus Operation S.A.S.","Airbus"],
 "UTC":["University of Technology of Compiègne"],
 "UZH":["University of Zurich","University of Zürich","Universität Zürich","University of Zurich and ETH Zurich"],
 "EPFL":["\u00c9cole Polytechnique F\u00e9d\u00e9rale de Lausanne","Blue Brain Project","EPFL","Swiss Plasma Center","École Polytechnique Fédérale de Lausanne","École polytechnique fédérale de Lausanne","Swiss Plasma Center"],
 "Biognosys AG":["Biognosys AG"],
 "ANSYS, Inc.":["ANSYS","ANSYS, Inc."],
 "CERN":["CERN"],
 "CNRS":["CNRS"],
 "AT&T Labs Research":["AT&T Labs – Research","AT&T Labs Research","AT&T Labs - Research"],
 "Ataturk University":["ATATÜRK UNIVERSITY'"],
 "AVL":["AVL, Graz","AVL List GmbH"],
 "CSCS":["CSCS","Swiss Centre of Scientific Computing","Swiss National Supercomputing Center"],
 "CHUV":["Center hospitalier universitaire vaudois"],
 "ETHZ":["ETH Zurich","Institute of Fluid Dynamics","Eidgenössische Technische Hochschule Zürich","ETH Zürich","ETH Zürich and Paul Scherrer Institute","ETH-Zentrum","ETHZ Computational Laboratory","University of Zurich and ETH Zurich","Institute of Fluid Dynamics","ETH-Zentrum","ETHZ Computational Laboratory"],
 "Eawag":["Eawag","Swiss Federal Institute of Aquatic Science and Technology"],
 "Fondazione Cardiocentro Ticino":["Fondazione Cardiocentro Ticino"],
 "HES-SO Valais-Wallis":["HES-SO//Valais-Wallis"],
 "IDSIA":["IDSIA"],
 "Idiap Research Institute":["Idiap Research Institute"],
 "Intel":["Intel","Intel Corporation","Intel Labs","Intel Labs and Carnegie Mellon University"],
 "MeteoSwiss":["MeteoSwiss"],
 "Ordecsys":["Ordecsys"],
 "Paul Scherrer Institute":["Paul Scherrer Institut","PSI"],
 "PMI":["Philip Morris International R&D"],
 "SIB":["SIB Swiss Institute of Bioinformatics","Swiss Institute of Bioinformatics"],
 "Stanford University":["Stanford University","Stanford University/NASA Ames"],
 "Supercomputing Systems AG":["Supercomputing Systems AG"],
 "Swiss Federal Institute of Technology":["Swiss Federal Institute of Technology"],
 "WLS":["Swiss Federal Research Institute WSL"],
 "Augsburg College":["Augsburg College"],
 "AUT":["Auckland University of Technology","Auburn University","University of Auckland"],
 "AUM":["Auburn University Montgomery"],
 "AIP-Astrophysikalisches Institut Potsdam":["Astrophysikalisches Institut Potsdam"],
 "Asbury University":["Asbury University"],
 "AREVA":["AREVA Nuclear Power"],
 "Asahikawa Medical University":["Asahikawa Medical University"],
 "Army Research Laboratory":["Army Research Laboratory","Army Research Office"],
 "ASU":["Arizona State University","Arizona State University and Los Alamos National Laboratory","University of Arizona","University of Arizona and Los Alamos National Laboratory"],
 "Aristotle University of Thessaloniki":["Aristotle University of Thessaloniki"],
 "Ariel University":["Ariel University"],
 "Argonne National Laboratory":["Argonne National Laboratory and the Illinois Institute of Technology","Argonne National Laboratory and University of Colorado Boulder","Argonne National Laboratory and University of Chicago","Argonne National Laboratory"],
 "Argo ParisTech":["Argo ParisTech"],
 "AMA, LLC":["Applied Mathematical Analysis, LLC"],
 "ALPEMI Consulting, LLC":["Alpemi Consulting, LLC"],
 "Rock Flow Dynamics, LLC":["Rock Flow Dynamics LLC"],
 "AB":["Applied Biomathematic"],
 "Georgia State University":["Georgia State University","Georgia College & State University",""],
 "Université de Versailles Saint-Quentin-en-Yvelines (UVSQ)":["Université de Versailles Saint-Quentin-en-Yvelines (UVSQ)","Versailles Saint-Quentin-en-Yvelines University","PRiSM - UVSQ"],
 "Appalachian State University":["Appalachian State University"],
 "Aoyama Gakuin University":["Aoyama Gakuin University"],
 "Antwerp University":["Antwerp University"],
 "Rio Tinto":["Rio Tinto","Rio Tinto Alcan and GERAD"],
 "Georgia Institute of Technology":["Georgia Insitute of Technology","Georgia Insitute of Technology"],
 "Google":["Google DeepMind","Google Pittsburgh","Google Research","Google and University of California, Santa Cruz","Google, Inc."],
 "Robert Bosch":["Robert Bosch GmbH"],
 "Angers University":["Angers University"],
 "Gifu Shotoku Gakuen University":["Gifu University"],
 "University of Bonn":["Bonn University","Rheinische Friedrich-Wilhelms-Universität Bonn","Universit&auml;t Bonn","Universitaet Bonn","University of Bonn","Universität Bonn"],
 "BIONAND":["Andalusian Centre for Nanomedicine and Biotechnology"],
 "Anadolu University":["Anadolu University"],
 "Amirkabir University of Technology":["Amirkabir University of Technology"],
 "Amherst College":["Amherst College"],
 "DLR":["German Aerospace Center (DLR)","German Aerospace Center, Oberpfaffenhofen"],
 "Australian National University":["Australian National University","Australian National Unversity, Canberra"],
 "Amgen Inc.":["Amgen Inc."],
 "Ames Laboratory":["Ames Laboratory"],
 "EDF":["EDF","EDF Energy R&D UK Centre","EDF Energy R&D UK Centre, IDCORE","EDF, Clamart"],
 "Alfréd Rényi Institute of Mathematics":["Alfréd Rényi Institute of Mathematics"],
 "AWI":["Alfred-Wegener-Institute for Polar and Marine Research","Alfred Wegener Institute"],
 "Bell Labs":["Alcatel-Lucent Bell Laboratories","Bell Laboratories, Alcatel-Lucent","Bell Laboratories, Lucent Technologies","Bell Labs","Bell Labs, Alcatel-Lucent"],
 "Ben Gurion University":["Ben Gurion University","Ben Gurion University Negev","Ben-Gurion University","Ben-Gurion University of the Negev"],
 "AAMU":["Alabama A&M University"],
 "Max Planck Institute":["Max Planck Insitute for Meteorology","Max Planck Institut Leipzig","Max Planck Institute for Biological Cybernetics","Max Planck Institute for Biophysical Chemistry","Max Planck Institute for Computer Science","Max Planck Institute for Dynamics of Complex Systems","Max Planck Institute for Dynamics of Complex Technical Systems","Max Planck Institute for Informatics","Max Planck Institute for Intelligent Systems","Max Planck Institute for Mathematics in the Sciences","Max Planck Institute for Molecular Biomedicine","Max Planck Institute for Plasma Physics","Max Planck Institute for Polymer Research","Max Planck Institute, Magdeburg","Max-Planck-Institut fuer Informatik","Max-Planck-Institut fuer Metallforschung","Max-Planck-Institut für Plasmaphysik","Max-Planck-Institute for Dynamics of Complex Technical Systems","Princeton Plasma Physics Laboratory"],
 "FGV EMAp":["EMAp/FGV"],
 "University of Wuppertal":["Bergische Universität","Bergische Universität Wuppertal","Bergische University"],
 "ENAC":["ENAC, Toulouse"],
 "HMS":["Beth Israel Deaconess Medical Center and Harvard Medical School"],
 "Erasmus University":["Erasmus Universiteit"],
 "Escuela Politecnica Nacional":["Escuela Politécnica Nacional"],
 "ENSEEIHT":["ENSEEIHT, Toulouse","ENSEEIHT-IRIT"],
 "European Centre for Medium-Range Weather Forecasts":["European Centre for Medium-Range Weather Forecasts","European Center for Medium Range Weather Forecasts"],
 "Ecole Normale Superieure":["Ecole Normale Supérieure","Ecole Normale Superieure","Ecole Nationale Superieure","École Normale Supérieure","École Normale Supérieure Paris"],
 "University of Freiburg":["Universität Freiburg","Universität Freiburg","Albert-Ludwigs Universität Freiburg","Albert-Ludwigs-Universitat Freiburg","Albert-Ludwigs University"],
 "Ecole des Ponts ParisTech":["École des Ponts ParisTech","Ecole Nationale des Ponts et Chaussées","Ecole des Ponts and Inria"],
 "Ecole Superieure de Chimie Physique Electronique de Lyon":["École Supérieure de Chimie Physique Électronique de Lyon","École Normale Supérieure de Lyon","Ecole Normale Superieure de Lyon","Ecole Centrale de Lyon"],
 "ESPCI ParisTech":["École Supérieure de Physique et de Chimie Industrielles"],
 "ENSAM ParisTech":["ENSAM, ParisTech"],
 "École Polytechnique de Montréal":["Ecole Polytechnique de Montréal","Mathematics and Industrial Engineering & GERAD, Ecole Polytechnique de Montreal","École Polytechnique de Montréal","Polytechnique Montreal"],
 "Ecole Polytechnique":["CMAP, Ecole Polytechnique","École Polytechnique","Ecole Polytechnique"],
 "École Centrale de Paris":["École Centrale de Paris","Ecole Centrale Paris"],
 "Ecole Centrale de Marseille":["École Centrale de Marseille"],
 "Ecole Normale Superieure de Cachan":["École Normale Supérieure de Cachan"],
 "Abo Akademi University":["Åbo Akademi University"],
 "The von Karman Institute for Fluid Dynamics":["von Karman Institute for Fluid Dynamics"],
 "Oakland University":["Oakland University, Michigan"],
 "iRhythm, Inc.":["iRhythm Technologies"],
 "eBay Labs":["eBay Research Labs"],
 "DSO":["DARPA/DSO"],
 "Otto-von-Guericke University":["Otto-von-Guericke-Universit&auml;t Magdeburg","Otto-von-Guericke-University Magdeburg","University of Magdeburg","Universität Magdeburg"],
 "Oregon State University":["Oregon State University and Mentor Graphics Corporation"],
 "Ohio University":["Ohio University and Brown University"],
 "Charles University":["Charles University","Charles University in Prague","Charles University, Prague"],
 "Centrum Wiskunde & Informatica":["Centrum Wiskunde & Informatica","Centrum Wiskunde & Informatica and University of Amsterdam","CWI, Amsterdam"],
 "Centrum voor Wiskunde en Informatica":["Centrum voor Wiskunde en Informatica","Centrum voor Wiskunde en Informatica (CWI)"],
 "The Catholic Univeristy of America":["Catholic University"],
 "California State University":["California State University, Chico","California State University, Dominguez Hills","California State University, Fresno","California State University, Fullerton","California State University, Long Beach","California State University, Los Angeles","California State University, Northridge","California State University, Sacramento","California State University, San Marcos","California State University, Stanislaus"],
 "California Polytechnic State University":["California Polytechnic State University","California Polytechnic State University, Pomona","California Polytechnic State University, San Luis Obispo"],
 "Jagiellonian University":["Jagiellonian University","Jagiellonian University, Krakow"],
 "Dartmouth College":["Dartmouth College","Dartmouth College and Simons Foundation"],
 "KAUST":["KAUST","KAUST Supercomputing Laboratory"],
 "Castel Research Inc.":["Castel Research Inc. and George Mason University"],
 "Jet Propulsion Laboratory":["Jet Propulsion Laboratory","Jet Propulsion Laboratory, California Institute of Technology"],
 "IMECC":["DMA-IMECC-UNICAMP"],
 "USGS Cascade Volcano Observatory":["USGS Cascades Volcano Observatory"],
 "Carnegie Institution for Science":["Carnegie Institution for Science and Stanford University"],
 "Universidad Carlos III de Madrid - UC3M":["Universidad Carlos III de Madrid","University Carlos III of Madrid","Universidad Carlos III","UC3M","Carlos III University"],
 "Keldysh Institute for Applied Mathematics":["Keldysh Institute for Applied Mathematics, RAS"],
 "KTH":["KTH Royal Institute of Technology","KTH Stockholm"],
 "CliSAP":["KlimaCampus - University of Hamburg"],
 "Delft University of Technology":["Delft University of Technology","Delft University of Technology and Shell International Exploration and Production","TU Delft","TU Eindhoven and TU Delft","Technical University of Delft","Technische Universität Delft","Delft University of Technology and Shell International Exploration and Production"],
 "D.A.V. College Pundri":["D. A. V. College Pundri"],
 "State University of New York-SUNY":["State University of New York at Buffalo","State University of New York, Brockport","State University of New York, Buffalo","State University of New York, New Paltz","State University of New York, Stony Brook","University of Buffalo","University of Buffalo, SUNY"],
 "D.E. Shaw Research":["D. E. Shaw Research","D. E. Shaw Research and Columbia University"],
 "KAUST":["King Abdullah University of Science & Technology (KAUST)"],
 "University of Linz":["University of Linz","Johannes Kepler University","Johannes Kepler Universität, Linz"],
 "BYU":["Brigham Young University"],
 "State Key Laboratory of Mechanical System and Vibration":["State Key Laboratory of Mechanical System and Vibration","State Key Laboratory of Mechanical System and Vibration, Shanghai Jiao Tong University"],
 "Kyoto University":["Kyoto University","Kyoto Prefectural University"],
 "Knust":["Kwame Nkrumah University of Science and Technology"],
 "Yerevan State University":["Yerevan State Universoty"],
 "DxO":["DxO Labs"],
 "Washington University":["Washington University","Washington University in St. Louis","Washington University, St. Louis","Washington and Lee University"],
 "YITP":["Yukawa Institute for Theoretical Physics, Kyoto"],
 "Yahoo! Inc.":["Yahoo! Inc.","Yahoo Japan Corporation","Yahoo! Labs","Yahoo! Research"],
 "Brigham & Women's Hospital":["Brigham & Women's Hospital","Brigham and Women's Hospital and Harvard Medical School"],
 "Boston University":["Boston University","Boston University and Harvard University"],
 "ExxonMobil Corporation":["Exxon","ExxonMobil","ExxonMobil Research","ExxonMobil Upstream Research Company"],
 "Eotvos Lorand University":["Eötvös Loránd University","Eötvös University"],
 "Ewha Womans University":["Ewha W. University"],
 "Rocsole":["Rocsole Ltd"],
 "CADFEM":["CADFEM GmbH"],
 "CDAC":["C-DAC, Agriculture College"],
 "Cenaero":["CENAERO"],
 "Cepel":["CEPEL"],
 "CEA":["CEA Saclay","CEA","CEA-Saclay","CEA/CESTA","CEA/DAM","CEA/DIF","CEA/DSM/IRFM Cadarache"],
 "CAEP Software Center":["CAEP Software Center for High Performance Numerical Simulations","CAEP Software Center for Numerical Simulation"],
 "Rennaisance Computing Institute":["Rennaisance Computing Institute (RENCI)"],
 "Vrije Universiteit Amsterdam":["Vrije Universiteit Amsterdam","VU University, Amsterdam"],
 "Virginia Polytechnic Institute":["Virginia Polytechnic Institute & State University","Virginia Polytechnic Institute and State University","Virginia Polytechnic Institute and State University and Wake Forest University"],
 "Virginia Tech":["Virginia Tech","Virginia Tech and Wake Forest University"],
 "Zhejiang University":["Zhejiang University","Zhejiang University City College"],
 "VSB-TUO":["VSB-Technical University Ostrava"],
 "Rolls-Royce Canada":["Rolls-Royce Canada Limited"],
 "RICAM":["RICAM, Austrian Academy of Sciences"],
 "RealEyes3D S.A.":["RealEyes3D"],
 "Shandong University":["Shandong University of Science and Technology"],
 "Shell Global":["Shell","Shell Exploration and Production Inc.","Shell Global Solutions International B.V., Rijswijk","Shell Global Solutions, Amsterdam","Shell Innovation Research & Development","Shell International Exploration & Production B.V.","Shell International Exploration and Production"],
 "Total":["Total","TOTAL SA","Total CSTGF","Total E&P"],
 "Lockheed Martin":["Lockheed-Martin","Lockheed Martin Advanced Technology Center","Lockheed Martin Coherent Technologies","Lockheed Martin Space Systems"],
 "Simons Foundation":["Simons Foundation and Courant Institute of Mathematical Sciences, New York University"],
 "Siemens":["Siemens AG","Siemens AG Corporate Technology","Siemens Corporation","Siemens Corporation Research"],
 "Southern Illinois University":["Southern Illinois University, Carbondale","Southern Illinois University, Edwardsville"],
 "Toyota Technological Institute":["Toyota Technological Institute","Toyota Technological Institute at Chicago"],
 "Simula Research Laboratory":["Simula Research Laboratory and University of Oslo"],
 "Tokyo University of Science":["Tokyo University of Science","Tokyo University of Science, Suwa"],
 "The Australian National University":["The Australian National University","The Australian National University and National ICT Australia Ltd"],
 "Texas State University":["Texas State University","Texas State University, San Marcos"],
 "Texas A&M University":["Texas A&M University","Texas A&M University and Indiana University","Texas A&M University, Corpus Christi"],
 "Mathematical Institute of Academy of Sciences":["Mathematical Institute ASCR, Prague"],
 "Loyola University-Chicago":["Loyola University of Chicago"],
 "MPI Saarbrücken":["MPII Saarbrücken"],
 "Massachusetts Institute of Technology":["Massachusetts Institute of Technology","Massachusetts Institute of Technology and Harvard Universit","Massachusetts Institute of Technology and Julia Computing"],
 "Martin Luther University Halle-Wittenberg":["Martin-Luther-University Halle-Wittenberg","Martin-Luther-Universität","University of Halle"],
 "LMU München":["Ludwig-Maximilians-Universität München"],
 "Tel Aviv University":["Tel Aviv University","Tel Aviv University and Microsoft Research"],
 "Massachusetts General Hospital":["Massachusetts General Hospital","Massachusetts General Hospital and Broad Institute","Massachusetts General Hospital and Harvard Medical School"],
 "Square Enix":["Square Enix Co. Ltd","Square Enix Research and Development Division"],
 "Monterrey Institute of Technology":["Tecnologico de Monterrey (ITESM)"],
 "RIKEN Advanced Institute for Computational Science":["RIKEN","RIKEN Advanced Institute for Computational Science","RIKEN Center for Advanced Intelligence Project","RIKEN Computational Science Research Program","RIKEN Genomic Sciences Center","RIKEN Institute of Physical and Chemical Research"],
 "RUTCOR":["RUTCOR - Rutgers University Center for Operations Research"],
 "RWTH Aachen":["RTWH Aachen","RWTH Aachen","RWTH Aachen University","RWTH-Aachen","RWTH - Aachen University of Technology"],
 "Brown University":["Brown University","Brown University and University of North Carolina, Chapel Hill","Brown University/Rhode Island School of Design (RISD)"],
 "BioAxial":["BioAxial","BioAxial and Université Paris Descartes"],
 "Rutgers University":["Rutgers University","Rutgers University, Camden","Rutgers University, New Brunswick","University of New Brunswick"],
 "Xi'an Jiaotong University":["Xi'an Jiaotong University","Xi'an Jiaotong - Liverpool University"],
 "Royal Liverpool":["Royal Liverpool and Broadgreen University Hospitals"],
 "Royal Institute of Technology":["KTH Royal Institute of Technology","Royal Institute of Technology","Royal Institute of Technology, Stockholm"],
 "Ruhr-University Bochum":["Ruhr-University Bochum","Ruhr-Universität Bochum","Ruhr-Universitat Bochum"],
 "Brandenburg University of Technology":["Brandenburg University of Technology","Brandenburgische Technische Universität Cottbus"],
 "Academy of Sciences of the Czech Republic, Prague":["Academy of Sciences of the Czech Republic, Prague","Institute of Mathematics of the Academy of Sciences of the Czech Republic","Academy of Sciences of the Czech Republic, Ostrava"],
 "Arts et Métiers ParisTech":["Arts et Metiers PARISTECH"],
 "Bordeaux INP":["Bordeaux Institute of Technology","Institut Polytechnique de Bordeaux"],
 "Centre Hospitalier Universitaire":["CHU Toulouse"],
 "CMM-Center Mathematical Modeling, Universidad de Chile":["CMM, Universidad de Chile"],
 "Spanish National Research Council (CSIC)":["CSIC, Madrid","IDAEA and Spanish National Research Council (CSIC)","IIM-CSIC, Vigo","Institut de Ciencia de Materials de Barcelona (ICMAB-CSIC)","Institute de Ciencias Matematicas-CSIC","Institute for Mathematics, CSIC"],
 "CALTECH-California Institute of Technology":["California Institute of Technology"],
 "Pontifical Catholic University of Chile":["Pontificia Universidad Católica de Chile","Catolica de Chile","Universidad Catolica de Chile"],
 "Coimbra University":["Coimbra University","Universidade de Coimbra","University Hospital of Coimbra","University of Coimbra"],
 "Czech Republic Academy of Science":["Czech Republic Academy of Science","Czech Academy of Sciences"],
 "Czech Technical University, Prague":["Czech Technical University, Prague","Czech Technical University"],
 "Durham University":["Durham University","University of Durham"],
 "MINES ParisTech":["Ecole des Mines de Paris","Mines ParisTech"],
 "Federal University of Rio Grande do Sul":["Federal University of Rio Grande do Sul","Universidade Federal do Rio Grande do Sul"],
 "Federal University of Sao Paulo":["Federal University of Sao Paulo","Universidade de Sao Paulo","University of Sao Paulo","University of São Paulo"],
 "Friedrich-Alexander University of Erlangen-Nuernberg":["Friedrich-Alexander Universitaet Erlangen-Nuernberg","Friedrich-Alexander-Universität Erlangen-Nürnberg","University Erlangen-Nuernberg","University Erlangen-Nürnberg","University of Erlangen","University of Erlangen","University of Erlangen-Nuernberg","University of Erlangen-Nuremberg","University of Erlangen-Nürnberg","Universität Erlangen","Universität Erlangen-Nürnberg"],
 "University of Göttingen":["University of Goettingen","Georg-August-Universität Göttingen"],
 "AUGUSTA University":["Georgia Regents University"],
 "Aalto University":["Helsinki University of Technology"],
 "Hong Kong Polytechnic University":["Hong Kong Polytechnic University","Chinese Academy of Engineering Physics (CAEP)"],
 "Humboldt University at Berlin":["Humboldt University at Berlin","Humboldt University Berlin","Humboldt State University"],
 "Institut d'Informatique et Mathematiques Appliquees-IMAG":["Institut d'Informatique et Mathematiques Appliquees","IMAG","LMC-IMAG, Grenoble"],
 "INSA de Rennes":["INSA de Rennes","Institut National des Sciences Appliquées de Rennes"],
 "IWR - University of Heidelberg":["IWR - University of Heidelberg","Interdisciplinary Center for Scientific Computing University Heidelberg"],
 "Institut Élie Cartan De Lorraine":["Institut Elie Cartan"],
 "IFP Energies nouvelles":["Institut Français du Pétrole","Institut Francais du Petrole"],
 "Universitat Autònoma de Barcelona - UAB":["Universitat Autònoma de Barcelona"],
 "Institute of Applied Physics and Computational Mathematics, Beijing":["Institute of Applied Physics and Computational Mathematics, Beijing","Institute of Applied Physics and Computational Mathematics"],
 "Institute for Geophysics":["Institute for Geophysics","Institute of Computational Mathematics and Mathematical Geophysics"],
 "Institute of High Performance Computing, A*STAR":["Institute of High Performance Computing, A*STAR","Institute of High Performance Computing"],
 "Institute of Information Technologies-SUPINFO":["Institute of Information Technologies"],
 "Institute of Mathematical Sciences, Chennai":["Institute of Mathematical Sciences, Chennai","Institute of Mathematical Sciences","Chennai Mathematical Institute"],
 "Institute of Science and Technology Austria":["Institute of Science and Technology Austria","Institute of Science and Technology","IST Austria, Klosterneuburg","IST"],
 "Johann Radon Institute for Computational and Applied Mathematics":["Johann Radon Institute for Computational and Applied Mathematics","Radon Institute for Computational and Applied Mathematics"],
 "Joseph Fourier University":["ISTerre, University Joseph Fourier","Joseph Fourier University","Universite Joseph Fourier","Universite Joseph Fourier and Inria","Université Joseph Fourier","Université Joseph Fourier and Inria"],
 "Zuse Institute Berlin (ZIB)":["Konrad -Zuse-Zentrum Berlin","Zuse Institute Berlin"],
 "Laboratoire d'analyse et d'architecture des systèmes":["LAAS-CNRS, Toulouse"],
 "Laboratoire Bordelais de Recherche en Informatique (UMR 5800)":["LABRI, Univ Bordeaux"],
 "Los Andes University":["Los Andes University","Universidad de los Andes"],
 "National Autonomous University of Mexico":["National Autonomous University of Mexico","Universidad Nacional Autonoma de Mexico"],
 "New York University-NYU":["New York University","Polytechnic Institute of New York University","Courant Institute of Mathematical Sciences, New York University","Courant Institute, New York University","Courant Institute of Mathematical Sciences","Courant Institute of Mathematical Sciences & Google Research"],
 "Newcastle University":["Newcastle University","University of Newcastle"],
 "University of Marburg":["University of Marburg","Philipps-Universität Marburg","Fachbereich Mathematik und Informatik, Philipps-Universität Marburg"],
 "Polytechnic University of Valencia":["Polytechnic University of Valencia","Polytechnical University of Valencia","Universidad Politecnica de Valencia","Universidad Politecnica de Valencia and Universidad Catolica de Valencia San Vicente Martir","Universitat Politecnica de Valencia","Universitat Politècnica de València"],
 "Polytechnical University of Bucharest":["Polytechnical University of Bucharest","University Politehnica of Bucharest"],
 "Pontifical Catholic University of Rio de Janeiro":["Pontifical Catholic University of Rio de Janeiro","Pontificia Universidade Catolica Do Rio de Janeiro"],
 "Preferred Networks":["Preferred Networks","Preferred Networks, Inc."],
 "Rey Juan Carlos University":["Rey Juan Carlos University","Universidad Rey Juan Carlos"],
 "University of Rome":["University of Rome La Sapienza","University of Rome","Sapienza – Università di Roma","Universita di Roma","Universita di Roma \"La Sapienza\'","Universita di Roma, La Sapienza","Università di Roma \"La Sapienza\"","Università di Roma I","Universitá di Roma I"],
 "Swansea University of South Wales":["Swansea University of South Wales","University of Wales Swansea"],
 "Technische Universität Berlin":["TU Berlin","Technical University Berlin","Technical University of Berlin","Technische Universitaet Berlin","Technische Universitat Berlin","Technische Universität Berlin","Technische Universität, Berlin"],
 "The Chinese University of Hong Kong":["The Chinese University of Hong Kong","Chinese University of Hong Kong"],
 "The City College of New York":["The City College of New York","City University of New York","City University of New York, Brooklyn","City University of New York, College of Staten Island","City University of New York, Staten Island","New York City College of Technology","New York Institute of Technology"],
 "The University of Chicago":["The University of Chicago","University of Chicago","University of Chicago and Argonne National Laboratory"],
 "The University of Texas at Austin":["The University of Texas at Austin","Texas Advanced Computing Center","University of Texas","University of Texas at Austin","University of Texas at Austin and Sandia National Laboratories","University of Texas, Austin","University of Texas MD Anderson Cancer Center","Institute for Computational Engineering and Sciences","Institute for Computational and Applied Mathematics","Institute for Geophysics"],
 "Thomas More College of Liberal Arts":["Thomas More College"],
 "Télécom ParisTech":["Télécom ParisTech","Telecom Paris"],
 "UPMC Sorbonne Universités":["UPMC Paris 6","Universite Pierre et Marie Curie (Paris 6)","Universite de Paris VI","University of Paris","University of Paris VI","Université Paris 6","Université Paris VI","Université Pierre et Marie Curie - Paris VI","École Normale Supérieure Paris","Institut Curie","University Pierre and Marie Curie (UPMC)","Université Pierre et Marie Curie","Université Pierre et Marie Curie and Inria","UPMC-Inria-TOTAL"],
 "Universidad Adolfo Ibáñez (UAI)":["Universidad Adolfo Ibáñez (UAI)","Universidad Adolfo Ibanez"],
 "Universidad Carlos III de Madrid - UC3M":["Universidad Carlos III de Madrid","University Carlos III of Madrid","Universidad Carlos III","UC3M","Carlos III University"],
 "Universidad Católica del Norte":["Universidad Católica del Norte","Universidad Catolica del Norte"],
 "Universidad Complutense de Madrid - UCM":["Universidad Complutense de Madrid"],
 "Universidad Católica del Norte":["Centrum voor Wiskunde en Informatica","Centrum voor Wiskunde en Informatica (CWI)"],
 "Universidad Politécnica de Madrid - UPM":["Universidad Politécnica de Madrid"],
 "USB-Università Simón Bolívar":["Universidad Simon Bolivar"],
 "UNIFEI-Universidade Federal de Itajubá":["Universidade Federal de Itajubá"],
 "UFMG - Universidade Federal de Minas Gerais":["Universidade Federal de Minal Gerais","Universidade Federal de Minas Gerais"],
 "Universidade Federal do Rio De Janeiro":["Universidade Federal do Rio De Janeiro","Universidade Federal de Rio de Janeiro","Federal University of Rio de Janerio"],
 "Federal University of the Triângulo Mineiro":["Universidade Federal do Triangulo Mineiro"],
 "Universidade de Lisboa":["Universidade de Lisboa","Universidade Técnica de Lisboa"],
 "Università degli Studi Di Palermo":["Universita degli Studi Di Palermo"],
 "Universita degli Studi di Firenze":["Universita degli Studi di Firenze","Universita' di Firenze","Università degli Studi di Firenze","University of Florence"],
 "University of Rome II, Tor Vergata":["University of Rome II, Tor Vergata","Universita di Roma \"Tor Vergata\"","Universita' di Roma II","Universita' di Roma Tor Vergata","Università degli Studi di Roma Tor Vergata"],
 "Università degli studi di Bergamo":["Universita' degli Studi di Bergamo"],
 "Università di Würzburg":["Universitaet Wuerzburg"],
 "University of Saarland":["University of Saarland","Saarland University","Universitaet des Saarlandes","Universität des Saarlandes"],
 "Universität zu Köln":["Universitaet zu Koeln"],
 "Universitat Autònoma de Barcelona - UAB":["Universitat Autònoma de Barcelona"],
 "Universidad Jaume I":["Universitat Jaume I","Universidad Jaume I"],
 "Universitat Politècnica de Catalunya":["Universitat Politècnica de Catalunya","Universitat Politecnica de Catalunya","Universidad Politecnica de Catalunya"],
 "Universitat Pompeu-Fabra, Barcelona - UPF":["Universitat Pompeu-Fabra, Barcelona","Universitat Pompeu Fabra"],
 "Universitat de les Illes Balears":["Universitat de les Illes Balears","Universitat Illes Balears"],
 "Université de Tours - Accueil":["Universite François Rabelais","University of Tours"],
 "Université Grenoble":["Universite Grenoble","Université Grenoble Alpes","Université de Grenoble I"],
 "University of Paris, Orsay":["Universite Paris 11","Universite de Paris-Sud","University of Paris, Orsay","University of Paris-Sud","Université Paris-Sud","University of Orsay","Université d'Orsay"],
 "Université Toulouse III  Paul Sabatier":["Centrum voor Wiskunde en Informatica","Centrum voor Wiskunde en Informatica (CWI)"],
 "University of Orléans":["Universite d'Orleans"],
 "Université de Franche-Comté":["Universite de Franche-Comte","Université de Franche-Comté & CNRS"],
 "Université  de Mons":["Universite de Mons"],
 "Université de Pau et des Pays de l'Adour":["Universite de Pau et des Pays de l'Adour","Universite de Pau"],
 "Université de Reims":["Universite de Reims"],
 "Université de Toulon":["Universite de Toulon"],
 "Université de la Nouvelle-Caledonia":["Universite de la Nouvelle-Caledonia"],
 "University of Klagenfurt":["University Klagenfurt","Universitat Klagenfurt","Alpen-Adria-Universität Klagenfurt"],
 "University of A Coruña":["University of A Coruña"],
 "University of Aarhus":["University of Aarhus","Aarhus University"],
 "University of Alabama":["University of Alabama","University of Alabama at Birmingham","University of Alabama, Birmingham","University of Alabama, Huntsville"],
 "University of Antwerp":["University of Antwerp","Antwerp University","Universiteit Antwerpen","University of Antwerp and IMEC"],
 "University of Augsburg":["University of Augsburg","Universität Augsburg"],
 "University of Aveiro":["University of Aveiro","Universidade de Aveiro"],
 "University of Barcelona":["Universitat de Barcelona","University of Barcelona"],
 "University of Bayreuth":["University of Bayreuth","University Bayreuth","Universität Bayreuth"],
 "University of Bielefeld":["University of Bielefeld","Bielefeld University","Universität Bielefeld"],
 "University of Bologna":["Universita' di Bologna","University of Bologna","Università di Bologna"],
 "University of Bordeaux":["Bordeaux University","Universite de Bordeaux I","University of Bordeaux","Université Bordeaux","Université Bordeaux I"],
 "University of Bremen":["University of Bremen","Center of Industrial Mathematics in Bremen","Universität Bremen"],
 "University of Brescia":["University of Brescia","Università degli Studi di Brescia"],
 "University of Caen":["University of Caen","Université de Caen","Université de Caen Basse Normandie"],
 "University of Cagliari":["University of Cagliari","Universita di Cagliari"],
 "University of Calabria":["University of Calabria","Università della Calabria"],
 "University of California":["University of California","University of California, Bakersfield","University of California, Berkeley","University of California, Davis","University of California, Irvine","University of California, Los Angeles","University of California, Merced","University of California, Riverside","University of California, San Diego","University of California, San Francisco","University of California, Santa Barbara","University of California, Santa Cruz","University of Southern California","University of Los Angeles","San Diego Supercomputer Center"],
 "University of Campinas":["State University of Campinas-Unicamp","Universidade Estadual de Campinas","Universidade de Campinas","University of Campinas"],
 "University of Cape Town":["University of Cape Town","University of Cape Town and South African Astronomical Observatory"],
 "University of Chile":["University of Chile","Universidad de Chile"],
 "University of Chinese Academy of Sciences":["University of Chinese Academy of Sciences","Chinese Academy of Sciences","Hong Kong University of Science and Technology"],
 "University of Colorado Boulder":["University of Colorado Boulder","University of Colorado"],
 "University of Colorado, Denver":["University of Colorado, Denver","University of Colorado at Denver"],
 "University of Copenhagen":["University of Copenhagen","Copenhagen University"],
 "University of Duisburg-Essen":["University Duisburg","University of Duisburg-Essen","Universität Duisburg-Essen"],
 "UEA-University of East Anglia":["University of East Anglia"],
 "The University of Edinburgh":["University of Edinburgh"],
 "University of Evry Val d'Essonne":["University of Evry-Val-d'Essonne","Evry University","Universite d'Evry Val d'Essone, Evry","Université Evry Val d'Essonne"],
 "University of Ferrara":["Universita' di Ferrara","University of Ferrara","Università degli Studi di Ferrara"],
 "University of Florida":["University of Florida","University of Florida, Gainesville"],
 "University of Frankfurt":["University of Frankfurt","Goethe University Frankfurt","Goethe University Frankfurt am Main","Goethe Universität Frankfurt","Johann Wolfgang Goethe University, Frankfurt am Main","Johann Wolfgang Goethe-Universität Frankfurt","J.W. Goethe-Universität","Goethe University"],
 "University of Genoa":["University of Genoa","University of Genova","Université de Genève"],
 "University of Glasgow":["University of Glasgow, Scotland"],
 "University of Graz":["University of Graz","Universität Graz","Karl Franzens University at Graz"],
 "University of Hamburg":["University of Hamburg","Universitat Hamburg"],
 "University of Göttingen":["Centrum voor Wiskunde en Informatica","Centrum voor Wiskunde en Informatica (CWI)"],
 "University of Hawaii":["University of Hawaii","University of Hawaii at Manoa"],
 "University of Heidelberg":["University of Heidelberg","University of Heidelberg and German Cancer Research Center","Universität Heidelberg","Heidelberg University"],
 "University of Hong Kong":["University of Hong Kong","Hong Kong University","Hong Kong University"],
 "University of Illinois, Chicago":["University of Illinois, Chicago","University of Ilinois at Chicago"],
 "University of Illinois, Urbana-Champaign":["University of Illinois, Urbana-Champaign","University of Illinois at Urbana-Champaign","University of Illinois","National Center for Supercomputing Applications, University of Illinois"],
 "University of Innsbruck":["University of Innsbruck","Universität Innsbruck"],
 "University of Iowa":["University of Iowa","The University of Iowa","Iowa State University"],
 "University of Kansas":["University of Kansas","University of Kansas, Lawrence"],
 "University of Karlsruhe":["University of Karlsruhe","Universität Karlsruhe"],
 "University of Kassel":["University Kassel","University of Kassel","Universität Kassel"],
 "University of Kiel":["University of Kiel","Kiel University"],
 "University of Konstanz":["University of Konstanz","Universität Konstanz"],
 "University of Kuopio":["University of Kuopio","Kuopio University"],
 "University of L'Aquila":["University of L'Aquila","Università degli Studi dell'Aquila","Università degli Studi dell'Aquil"],
 "University of La Laguna":["University of La Laguna","University La Laguna"],
 "National University of La Plata ":["National University of La Plata ","University of La Plata"],
 "University of Lancaster":["University of Lancaster","Lancaster University"],
 "University of Leeds":["University of Leeds","Leeds University"],
 "University of Leiden":["University of Leiden","Leiden University"],
 "University of Leipzig":["University of Leipzig","Universität Leipzig"],
 "University of Lille":["University of Lille","Université Lille 1 and CNRS","Universite des Sciences et Technologies de Lille"],
 "University of Limoges":["University of Limoges","Université de Limoges","Limoges University"],
 "University of Lisbon":["University of Lisbon","Instituto Superior Tecnico"],
 "University of Lorraine":["University of Lorraine","Université de Lorraine"],
 "University of Lübeck":["University of Luebeck","Universitaet zu Luebeck"],
 "University of Lund":["University of Lund","Lund University"],
 "University of Maastricht":["University of Maastricht","Maastricht University"],
 "University of Mainz":["University of Mainz","Johannes Gutenberg-Universität, Mainz"],
 "University of Manchester":["University of Manchester","The University of Manchester"],
 "University of Mannheim":["University of Mannheim","Universitaet Mannheim"],
 "University of Maryland":["University of Maryland","University of Maryland, College Park"],
 "University of Massachusetts":["University of Massachusetts","University of Massachusetts, Amherst","University of Massachusetts, Boston","University of Massachusetts, Dartmouth","University of Massachusetts, Lowell"],
 "University of Michigan":["University of Michigan","The University of Michigan, Ann Arbor","University of Michigan, Ann Arbor","University of Michigan, Dearborn","University of Michigan-Flint"],
 "University of Minnesota":["University of Minnesota","University of Minnesota and Army HPC Research Center","University of Minnesota, Minneapolis","University of Minnesota, Twin Cities","IMA, University of Minnesota","Institute for Mathematics and its Applications, University of Minnesota","Institute for Mathematics and its Applications"],
 "University of Modena and Reggio Emilia":["Universita degli Studi di Modena e Reggio Emilia","Universita di Modena e Reggio Emilia","University of Modena and Reggio Emilia"],
 "University of Montreal":["University of Montreal","Universite de Montreal","Université de Montréal"],
 "University of Münster":["University of Münster","Universität Münster"],
 "University of Naples":["University of Naples","University of Naples \"Frederico II\", Naples","University of Napoli","Parthenope University, Napoli","University of Napoli","Università degli Studi di Napoli Federico II","Università di Napoli"],
 "University of Nebraska, Lincoln":["University of Nebraska, Lincoln","University of Nebraska-Lincoln"],
 "University of Neuchatel":["University of Neuchatel","Universite de Neuchatel"],
 "University of Nevada":["University of Nevada","University of Nevada, Reno"],
 "University of New Mexico":["University of New Mexico","New Mexico State University"],
 "University of New South Wales":["University of New South Wales","University of New South Wales, Sydney"],
 "University of North Carolina at Chapel Hill":["University of North Carolina at Chapel Hill","NIEHS and University of North Carolina, Chapel Hill","North Carolina A&T State University","University of North Carolina","University of North Carolina at Chapel Hill and University of Warwick","University of North Carolina, Chapel Hill"],
 "University of Nottingham":["University of Nottingham","Nottingham University"],
 "University of Oklahoma":["University of Oklahoma","Oklahoma State University"],
 "University of Oslo-UiO":["University of Oslo"],
 "University of Osnabrueck":["University of Osnabrück"],
 "University of Oxford":["University of Oxford","Oxford e-Research Centre","Oxford University"],
 "University of Paderborn":["University of Paderborn","Universität Paderborn"],
 "University of Paris, Dauphine":["CEREMADE Universite Paris 9 Dauphine","Universite Paris 9 Dauphine","Universite Paris Dauphine and CNRS","University of Paris, Dauphine","Université Paris Dauphine"],
 "University of Parma":["University of Parma","Universita degli Studi di Parma"],
 "University of Pavia":["Universit&agrave; degli Studi di Pavia","University of Pavia","Università di Pavia"],
 "University of Pisa":["Universita di Pisa","Universita' di Pisa","University of Pisa","Università di Pisa"],
 "University of Pittsburgh":["University of Pittsburgh","University of Pittsburgh, Johnstown"],
 "University of Poitiers":["University of Poitiers","Université de Poitiers"],
 "University of Puerto Rico":["University of Puerto Rico","University of Puerto Rico, Cayey"],
 "University of Puerto Rico at Mayagüez":["University of Puerto Rico, Mayaguez"],
 "University of Quebec, Montreal":["University of Quebec, Montreal","Universite du Quebec a Montreal"],
 "University of Reading":["University of Reading","University of Reading and Cray Inc."],
 "University of Regensburg":["Universit\"at Regensburg","University of Regensburg","Universität Regensburg"],
 "University of Science and Technology of China":["University of Science and Technology of China","University of Science & Technology","Joint Advanced Research Center of University of Science and Technology of China and City Universi…"],
 "University of Sciences and Technology-Houari":["University of Sciences and Technology Houari"],
 "University of Seville":["University of Seville","University of Sevilla","Universidad de Sevilla"],
 "University of Sherbrooke":["University of Sherbrooke","Universite de Sherbrooke"],
 "University of Siegen":["University of Siegen","Universität Siegen"],
 "University of Southern Denmark-SDU":["University of Southern Denmark"],
 "University of St. Thomas":["University of St. Thomas","University of Houston"],
 "University of Stellenbosch":["University of Stellenbosch","Stellenbosch University"],
 "University of Strasbourg":["University of Strasbourg","Université de Strasbourg"],
 "University of Tennessee":["University of Tennessee","University of Tennessee and Oak Ridge National Laboratory","University of Tennessee, Knoxville","National Institute for Computational Sciences"],
 "UT Southwestern Medical Center":["University of Texas Southwestern Medical Center at Dallas"],
 "The University of Texas at El Paso - UTEP":["University of Texas at El Paso","University of Texas, El Paso"],
 "University of Texas, Dallas":["University of Texas, Dallas","University of Texas at Dallas","The University of Texas at Dallas and City University of Hong Kong"],
 "University of Toronto":["University of Toronto","University of Toronto Institute for Aerospace Studies"],
 "University of Toulouse":["Universite de Toulouse","University of Toulouse","Université of Toulouse","Institut Supérieur de l'Aéronautique et de l'Espace"],
 "Université Toulouse III - Paul Sabatier":["University of Toulouse III","Universite Paul Sabatier"],
 "University of Trento":["University of Trento","Università degli Studi di Trento"],
 "University of Trier":["Trier University","Universitaet Trier","University of Trier","Universität Trier"],
 "University of Trieste":["University of Trieste","Universita di Trieste","Universita` degli Studi di Trieste"],
 "University of Tübingen":["University of Tübingen","Universität Tübingen"],
 "University of Utah":["University of Utah","Utah Center for Advanced Imaging Research"],
 "University of Valencia":["University of Valencia","Universitad de Valencia","Universitat de Valencia"],
 "University of Valladolid":["University of Valladolid","Universidad de Valladolid"],
 "University of Verona":["University of Verona","Universita di Verona"],
 "University of Vienna":["University of Vienna","Universität Wien"],
 "University of Wageningen":["University of Wageningen","Wageningen Universiteit"],
 "University of Warsaw":["University of Warsaw","University of Warsaw and Nicolaus Copernicus University in Torun","Warsaw University","Warsaw University of Technology"],
 "University of Warwick":["University of Warwick","Warwick University"],
 "University of Washington":["University of Washington","University of Washington, Seattle"],
 "University of Wisconsin":["University of Wisconsin","University of Wisconsin, Madison","the University of Wisconsin","the University of Wisconsin-Madison"],
 "University of Wroclaw":["University of Wroclaw","Uniwersytet Wroclawski"],
 "University of Würzburg":["University of Würzburg","Universität Würzburg","Wurzburg University"],
 "University of Yamanashi":["University of Yamanashi","Yamanashi University"],
 "University of the Littoral Opal Coast":["University Littoral Cote d’Opale, Calais","University of the Littoral Opal Coast","Université du Littoral Calais Cedex"],
 "University of the West Indies":["University of the West Indies","The University of the West Indies"],
 "Università degli Studi Roma Tre":["University of Rome III","Università degli Studi Roma Tre","Universita di Roma Tre"],
 "University of Stuttgart":["Stuttgart University","Universit&auml;t Stuttgart","University of Stuttgart","Universität Stuttgart","Institut fuer Aerodynamik und Gasdynamik (IAG)"],
 "Université Catholique de Louvain":["Université Catholique de Louvain","Universite Catholique de Louvain","University of Louvain"],
 "Université Claude Bernard Lyon 1":["Université Claude Bernard Lyon 1","Universite de Lyon 1","University of Lyon 1"],
 "Université Clermont Auvergne":["Université Clermont Auvergne","Universite Blaise Pascal"],
 "University of Mentouri Brothers- Constantine":["University of Brothers Mentouri","Université Mentouri Constantine"],
 "Université Paris 13":["Universite Paris-Nord","Université Paris 13","Université Paris XIII","Université de Paris Nord"],
 "Université Paris Descartes":["Paris Descartes","Universite Paris 5","Université Paris Descartes","Université de Paris Descartes","Universite Rene Descartes"],
 "Université Paris-Diderot":["Universite Paris 7-Denis Diderot","Université Paris VII","Université Paris VII - Denis Diderot","Université Paris-Diderot"],
 "UPEC - Université Paris-Est Créteil Val de Marne":["Universite de Paris XII","Universite de Paris-Est","Université Paris-Est","Université Paris-Est Créteil Val de Marne","Université Paris-est Créteil"],
 "Université Toulouse I Capitole":["Université Toulouse I"],
 "Université d'Aix-Marseille III":["Université d'Aix-Marseille III","Universite Paul Cezanne"],
 "Université de Montpellier":["Université de Montpellier","Université Montpellier II","Universite de Montpellier II"],
 "Université de Nice, Sophia Antipolis":["Université de Nice, Sophia Antipolis","University of Nice Sophia-Antipolis and Inria","University of Nice"],
 "Université de Rennes 1":["Université de Rennes 1","Institute of Mathematical Research of Rennes","University of Rennes 1 and Inria Rennes","Université de Rennes 1 & Inserm"],
 "Université de Rouen":["Université de Rouen","Universite de Rouen"],
 "Université de Saint-Etienne":["Université de Saint-Etienne","Universite de Saint-etienne"],
 "Utrecht University":["University of Utrecht","Utrecht University"],
 "Vienna University of Technology":["Vienna University of Technology","Technische Universitat Vienna","TU Wien","Technische Universitaet Wien","Technische Universität Wien"],
 "Weierstrass Institute for Applied Analysis and Stochastics":["WIAS, Berlin","WIAS-Berlin","Weierstrass Institute for Applied Analysis and Stochastics, Berlin","Weierstrass Institute for Applied Analysis and Stochastics","Weierstrass Institute for Applied Analysis and Stochastics, Berlin"],
 "École Normale Supérieure de Lyon":["Université de Lyon","École Normale Supérieure de Lyon","ENS Lyon","Ecole Centrale de Lyon","Ecole Normale Superieure de Lyon","École Supérieure de Chimie Physique Électronique de Lyon","Institut Camille Jordan"],
 "École normale supérieure Paris-Saclay":["École Normale Supérieure de Cachan","LMT-Cachan","Ecole Normale Supérieure de Cachan","Ecole Normale Superieure de Cachan","Ecole Normale Superieur de Cachan","ENS Cachan","CMLA, ENS de Cachan"],
 "Concordia University":["Concordia University","Concordia College"],
 "GAMS Development Corporation":["GAMS Development Corporation","GAMS Software GmbH"],
 "Harvard University":["Harvard University","Harvard Medical School","Harvard, Smithsonian Center for Astrophysics"],
 "Shanghai Jiao Tong University":["Shanghai Jiao Tong University","Shanghai Jiaotong University"],
 "Shanghai University":["Shanghai University","Shanghai University of Finance and Economics"],
 "South China University of Technology":["South China University of Technology","South China Normal University"],
 "EADS Innovation Works":["EADS Innovation Works","Eads Innovation Works"],
 "Istituto per le Applicazioni del Calcolo Mauro Picone-IAC":["Istituto per le Applicazioni del Calcolo \"Mauro Picone\"","Istituto per le Applicazioni del Calcolo \"Mauro Picone\""],
 "Jülich Supercomputing Centre (JSC)":["Jülich Research Centre","Jülich Supercomputing Centre"],
 "King Abdullah University of Science and Technology":["KAUST"]}

'''##############################
         HELPER FUNCTIONS
################################# '''

# Remove unnecessary content and excess spaces
def to_plane_text(fileLine):
   fileLine = (re.sub(' +',' ', fileLine.replace('\t','').replace('<em>', '').replace('<EM>', '').replace('</em>', '').replace('</EM>', '').replace('<img src="../updated.gif" alt="updated">', '')))
   return fileLine

# def _func_str_to_unicode(s):
#    return s.encode('ascii', 'ignore').decode('ascii')

# Take only the Switzerland researchers and same them temporarily in a file
def split_lines(fileLine):
   if (not ((',</s>' not in fileLine) and (',</S>' not in fileLine) and ('</EM></s>' not in fileLine) and ('</em></s>' not in fileLine) and (not fileLine.endswith(',')))):
      return ""
   else:
      return fileLine.replace('</s>','').replace('</S>','')

def strcmp(name1,name2):
   # if(len(name1) != len(name2)):
   #    print len(name1)
   #    print len(name2)
   #    return 0
   m = min(len(name1),len(name2))
   # print "CS " + name1[0]
   # print "CS " + name1[1]
   # print "CS " + name1[2]
   # print "CS " + name1[3]
   for i in range(0, m):
      if(name1[i]!=name2[i]):
         # print name1[i]
         # print name2[i]
         return 0
   return 1

def adjust_university(uni, uni_map):
   newuni = re.sub(' +',' ', uni).rstrip().lstrip()
   for i in uni_map:
      for j in uni_map[i]:
         if(newuni.encode('latin_1')==j):
            return i
   return newuni.encode('latin_1')

# Helper function that adjust names of university
def adjust_university_pasc(uni):
   uni = re.sub(' +',' ', uni)
   uni = uni.replace('Zürich', 'Zurich')
   uni = uni.replace('Institut ', 'Institute ')
   uni = uni.replace('Institutee', 'Institute')
   uni = uni.replace('Berne', 'Bern')
   uni = uni.replace('Bernee', 'Bern')
   uni = uni.replace('Universität', 'University of')
   uni = uni.replace('Université de Genève', 'University of Geneva')
   uni = uni.replace('Philip Morris Int.','Philip Morris International R&D')
   uni = uni.replace('IBM Research - Zurich','IBM Research')
   uni = uni.replace('IBM Research - Zürich','IBM Research')
   uni = uni.replace('IBM Research-Zürich','IBM Research')
   uni = uni.replace('Univeristy', 'University')
   uni = uni.replace('Universite de', 'University of')
   uni = uni.replace('Eidgenössische Technische Hochschule','ETH')
   uni = uni.replace('École Polytechnique Fédérale de Lausanne','EPFL')
   uni = uni.replace('Università della Svizzera italiana', 'USI')
   uni = uni.replace('Università della Svizzera Italiana', 'USI')
   uni = uni.replace('University of Lugano','USI')
   uni = uni.replace('Centre','Center')
   uni = uni.replace('polytechnique f','Polytechnique F')
   uni = uni.replace('and ', ' ').rstrip().lstrip()
   return uni

# Extract names from pasc conferences and insert them in
# json data['authors']
def take_names_pasc(co_organisers, uni_map_p):
   for x in co_organisers:
      if "Switzerland" in x:
         information = x.split('(')
         name = information[0].rstrip().lstrip()
         name = re.sub(' +',' ',name)
         information[1] = information[1].replace('Philip Morris International R&D','Philip Morris Int.')
         if('HES-SO' in information[1]):
            universities = information[1].split(',')
         elif ('Netherlands' in information[1]):
            universities = [information[1].split('&')[0]]
         else:
            universities = re.split(';|/|&|,', information[1]);
         for x in universities:
            if('Switzerland)' in x):
               break
            if('Switzerland' in x):
               continue
            university = x.split(',')[0].rstrip().lstrip()
            university = re.sub(' +',' ',university)
            university = adjust_university_pasc(university)
            university = adjust_university(university.decode('latin_1'), uni_map_p)
            nu = name + '\t' + university.decode("latin_1").encode("latin_1") +'\tSwitzerland'
            if (nu not in names):
               if(university != "TODELETE"):
                  names.append(nu)

   for count in range(0,len(names)):
      coauthors = list(names)
      coauthors.remove(names[count])
      if(check_if_name_exists(data, names[count])):
         s = names[count].split('\t')
         # print "106 " +s[1]
         data['authors_swiss'].append({'name': s[0], 'university':s[1], 'nation':s[2], 'coauthors': coauthors})
      else:
         for c in coauthors:
            check_if_coauthor_exists_or_add(data, names[count], c)
   return

# Check if the name has been already saved in json data['authors']
# If not we save it
def check_if_name_exists(data, nu):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            return 0
    for x in data['authors_swiss']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            return 0
    return 1

def check_if_name_exists_with_nation(data, nu):
    s = nu.split('\t')
    for x in data:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            return 0
    return 1

def check_if_name_exists_no_nation(data, nu):
   s = nu.split('\t')
   for x in data:
      if x['name']==s[0] and x['university']==s[1]:
           return 0
   return 1

# If the name of the author is already present in json data['authors'],
# check if there are some coauthors to add
def check_if_coauthor_exists_or_add(data, nu, coauthor_name):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            for coauthor in x['coauthors']:
                if(coauthor.rstrip().lstrip() == coauthor_name.rstrip().lstrip()):
                    return 0
            x['coauthors'].append(coauthor_name)
    for x in data['authors_swiss']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            for coauthor in x['coauthors']:
                if(coauthor.rstrip().lstrip() == coauthor_name.rstrip().lstrip()):
                    return 0
            x['coauthors'].append(coauthor_name)
    return 1

# Organizes the coauthors list such that we have an array of :
# {'name': coauthor_name, 'university': coauthor_university}
def adjust_coauthors(coauthors):
   res = []
   for e in coauthors:
      s = e.split('\t')
      s[2] = s[2].replace(';','')
      s[2] = re.sub(' +',' ', s[2]).rstrip().lstrip()
      s[1] = re.sub(' +',' ', s[1]).rstrip().lstrip()
      s[0] = re.sub(' +',' ', s[0]).rstrip().lstrip()
      res.append({'name': s[0], 'university':s[1], 'nation':s[2]})
   return res

# If the author is already in author_names['authors']
# take its index
def take_index(data, nu):
    s = nu.split('\t')
    for count in range(0,len(data)):
        if data[count]['name']==s[0] and data[count]['university']==s[1]:
            return count+1
    return -1

# Write in the edges file all the connection between authors
# such as (first_author_index,second_author_index)
def make_edges(id, ids, file):
   for i in ids:
      if(id != i):
         file.write('('+str(id)+','+str(i)+')\n')

def adjust_name(name):
   name = name.replace(',', '').replace(' and', '').replace('and ', '')
   return name


'''##############################
      END HELPER FUNCTIONS
################################# '''


# FIRST PART: take all the necessary information and save them in a file
# Open the file with all html pages "apache-nutch-1.14/dump/dump"
file = open("../nutch_crawler/apache-nutch-1.14/dump/dump","r")
# Read the file
content = file.read()


# Make the regex: we want to take all <dd> elements that can
# end with <dt> or </dl>
# re.MULTILINE|re.DOTALL allow to take multiline text
regex = re.compile("<dd>(.*?)((<dt>)|(</dl>))",  re.MULTILINE|re.DOTALL)

# find all matching strings with the regex
all_matching = re.findall(regex, content)
all_matching = [x[0] for x in all_matching]
# transform all matching strings in the format required
all_matching = map(to_plane_text, all_matching)

# Split the lines and write them in the file
all_matching = map(split_lines, all_matching)

# close used files
file.close()


# SECOND PART: take the information, extract a list of names
# with their universities
file_output = open("authors.json", "w")
file_output.truncate()

data = {}
data['authors'] = []
data['authors_swiss'] = []

regex_universities = re.compile(",(.*?) and (.*?),")

uni_to_delete = [['German Aerospace Center (DLR)', ' Simulation'],
                 ['University of Tennessee', ' ORNL'],
                 ['University of California', ' Berkeley'],
                 ['Institute of Mathematics', ' Physics'],
                 ['University of California', ' Los Angeles - IPAM'],
                 ['Institut f\xc3\xbcr Numerische Simulation', ' Universit\xc3\xa4t Bonn'],
                 ['Chinese University of Hong Kong', ' Hong Kong'],
                 ['Indian Institute of Space', ' Science'],
                 ['Charles University', ' Prague;'],
                 ['University of California', ' Davis'],
                 ['Institut f\xc3\xbcr Numerische Simulation', ' Universit\xc3\xa4t Bonn'],
                 ['Khalifa University of Science', ' Technology'],
                 ['University of Wisconsin', ' Madison']]



# For each line we extract the names with relative universities,
# and we organized the results in a json file with a list of authors
# Each author has a name, a university and a list of coauthors
for y in all_matching:
   k = y.split('\n')
   k = filter(lambda x: x!="", k)
   if(len(k)>1):
      j =[]
      i=0
      l=[]
      for elem in k:
         if(';'in elem):
            l.append(elem)
            j.append(l)
            l=[]
         else:
            l.append(elem)
      if(l):
         j.append(l)
      names = []
      for elem in j:
         info = elem[len(elem)-1]
         elem.remove(elem[len(elem)-1])
         names_list = map(adjust_name, elem)
         multiple_uni = re.findall(regex_universities, info)
         if(multiple_uni):
            if((info.count(" and "))==1):
               info.replace(', and ', ' and ')
               unis = info.split(',')
               uni=[]
               universities = []
               for elem in unis:
                  if(' and ' not in elem):
                     uni.append(elem)
                  else:
                     uni.append(elem.split(' and ')[0])
                     uni = filter(lambda x: x!="", uni)
                     if(len(uni)==2) and (uni not in uni_to_delete):
                        universities.append(uni[0]+'\t'+uni[1])
                     uni = [elem.split(' and ')[1]]
               if(len(uni)==2)and (uni not in uni_to_delete):
                  universities.append(uni[0]+'\t'+uni[1])
            else:
               universities = []
         else:
            unis = info.split(',')
            unis = filter(lambda x: x!="", unis)
            unis = filter(lambda x: x!=" ", unis)
            if(len(unis)==1):
               universities = []
            elif(len(unis)==2):
               universities = []
               universities.append(unis[0]+'\t'+unis[1])
            elif(len(unis)==3):
               universities = []
               universities.append(unis[0]+','+unis[1]+'\t'+ unis[2])
            else:
               universities = []

         if(names_list and universities):
            for n in names_list:
               for u in universities:
                  n = re.sub(' +',' ', n).rstrip().lstrip()
                  u = u.split('\t')
                  u[1] = u[1].replace(';','')
                  if(n and u[0] and u[1]):
                     if(u[1] == 'The Netherlands'):
                        u[1] = 'Netherlands'
                     if(u[1] == 'Saudia Arabia'):
                        u[1] = 'Saudi Arabia'
                     u[0] = adjust_university(u[0].decode('latin_1'),uni_map)
                     u[1] = u[1].rstrip().lstrip()
                     nn = n+'\t'+u[0].decode('latin-1').encode('latin-1')+'\t'+u[1]
                     if(nn not in names):
                        if(u[0] != "TODELETE"):
                           names.append(nn.rstrip().lstrip())

      for count in range(0,len(names)):
         coauthors = list(names)
         coauthors.remove(names[count])
         if(check_if_name_exists(data, names[count])):
            s = names[count].split('\t')
            if ('Switzerland' in s[2]):
               data['authors_swiss'].append({'name': s[0], 'university':s[1], 'nation':s[2], 'coauthors': coauthors})
            else:
               s[2] = s[2].replace(';','')
               s[2] = re.sub(' +',' ', s[2]).rstrip().lstrip()
               s[1] = re.sub(' +',' ', s[1]).rstrip().lstrip()
               data['authors'].append({'name': s[0], 'university':s[1], 'nation':s[2], 'coauthors': coauthors})
         else:
            for c in coauthors:
               check_if_coauthor_exists_or_add(data, names[count], c)



# THIRD PART: take two html pages with a regex about pasc conferences
# Open the file with all html pages "apache-nutch-1.14/dump2/dump"
file = open("../nutch_crawler/apache-nutch-1.14/dump2/dump","r")
# Read the file
content = file.read()


# re.MULTILINE|re.DOTALL allow to take multiline text
regex = re.compile("<!DOCTYPE html(.*?)</html>",  re.MULTILINE|re.DOTALL)

# find all matching strings with the regex
all_matching = re.findall(regex, content)


if(not (("<base href=\"http://www.pasc15.org/\" />" in all_matching[0]) and ("<base href=\"http://www.pasc16.org/\" />" in all_matching[1]))):
    sys.exit()

# Regex for pasc conferences
regex_pasc = re.compile("<!-- new symposium(.*?)<!-- end symposium abstract",  re.MULTILINE|re.DOTALL)
programs = re.findall(regex_pasc, all_matching[0])
programs2 = re.findall(regex_pasc, all_matching[1])
programs = programs + programs2

# Take all the names from pasc conferences' pages
for i in programs:
	names = []
	regex_organiser = re.compile("Organiser:</td>(.*?)<td>(.*?)</td>",  re.MULTILINE|re.DOTALL)
	regex_co_organiser = re.compile("Co-organiser:</td>(.*?)<td>(.*?)</td>",  re.MULTILINE|re.DOTALL)
	regex_table = re.compile("<!-- begin single abstract programm(.*?)</tr>",  re.MULTILINE|re.DOTALL)

	organiser = re.findall(regex_organiser, i)
	co_organisers = re.findall(regex_co_organiser, i)
	table = re.findall(regex_table, i)

	organiser = [x[1] for x in organiser][0]
	co_organisers = [x[1] for x in co_organisers][0]

	co_organisers = co_organisers.split(');')
	co_organisers.append(organiser)

	regex_elem = re.compile("</strong>,(.*?)\)",  re.MULTILINE|re.DOTALL)
	for y in table:
		elem = re.findall(regex_elem, y)[0]
		co_organisers.append(elem)
	take_names_pasc(co_organisers, uni_map)


# FOURTH PART: adjust coauthors to save all in a file
for elem in data['authors']:
   elem['coauthors'] = adjust_coauthors(elem['coauthors'])
for elem in data['authors_swiss']:
   elem['coauthors'] = adjust_coauthors(elem['coauthors'])


# Save all in the output file
json.dump(data, file_output)

file_output.close()


# FIFTH PART: take the information in the json file and create a file
# containing the "edges" between coauthors

file_json = open('authors.json')
data_json = json.load(file_json)
swiss_information = open("swiss_information.json", "w")
edges_swiss = open("edges_swiss.txt", "w")
world_information = open("world_information.json", "w")
edges_world = open("edges_world.txt", "w")

author_indexes_swiss=[]
author_indexes=[]

information = {}
information['authors_swiss'] = []
information['universities_swiss'] = []
information['authors'] = []
information['universities'] = []
index = 1;

# print len(information['universities_swiss'])

# Edges for swiss
for idx in range(0,len(data_json['authors_swiss'])):
   name = data_json['authors_swiss'][idx]['name']
   university = data_json['authors_swiss'][idx]['university']
   nu = name+'\t'+university

   if(check_if_name_exists_no_nation(information['authors_swiss'], nu)):
      information['authors_swiss'].append({'index': index, 'name': name, 'university': university})
      # print university
      information['universities_swiss'].append(university)
      # print information['universities_swiss']
      author_id = index
      index = index+1
   else:
      for x in information['authors_swiss']:
          if x['name']==name and x['university']==university:
              author_id = x['index']

   author_indexes_swiss.append(author_id)
   coauthor_indexes = []
   for author in data_json['authors_swiss'][idx]['coauthors']:
      if(author['nation']=='Switzerland'):
         nn = author['name']+'\t'+author['university']
         if(check_if_name_exists_no_nation(information['authors_swiss'], nn)):
            information['authors_swiss'].append({'index': index, 'name': author['name'], 'university': author['university']})
            # print author['university']
            information['universities_swiss'].append(author['university'])
            # print information['universities_swiss']
            coauthor_indexes.append(index)
            index = index+1
         else:
            id = take_index(information['authors_swiss'], nn)
            if(id not in author_indexes_swiss):
               coauthor_indexes.append(id)

   make_edges(author_id, coauthor_indexes, edges_swiss)


# Edges from all the world
all_names = data_json['authors_swiss']+data_json['authors']
index = 1;

for idx in range(0,len(all_names)):
   name = all_names[idx]['name']
   university = all_names[idx]['university']
   nation = all_names[idx]['nation'].rstrip().lstrip()
   nu = name+'\t'+university+'\t'+nation

   if(check_if_name_exists_with_nation(information['authors'], nu)):
      information['authors'].append({'index': index, 'name': name, 'university': university, 'nation': nation})
      information['universities'].append(university)
      author_id = index
      index = index+1
   else:
      for x in information['authors']:
          if x['name']==name and x['university']==university and x['nation']==nation:
              author_id = x['index']

   author_indexes.append(author_id)
   coauthor_indexes = []
   for author in all_names[idx]['coauthors']:
      nn = author['name']+'\t'+author['university']+'\t'+author['nation'].rstrip().lstrip()
      if(check_if_name_exists_with_nation(information['authors'], nn)):
         information['authors'].append({'index': index, 'name': author['name'], 'university': author['university'], 'nation': author['nation']})
         information['universities'].append(author['university'])
         coauthor_indexes.append(index)
         index = index+1
      else:
         id = take_index(information['authors'], nn)
         if(id not in author_indexes):
            coauthor_indexes.append(id)

   make_edges(author_id, coauthor_indexes, edges_world)

swiss_file = {'names':information['authors_swiss'],'universities':information['universities_swiss']}
json.dump(swiss_file, swiss_information)

world_file = {'names':information['authors'],'universities':information['universities']}
json.dump(world_file, world_information)

file_json.close()
swiss_information.close()
edges_swiss.close()
world_information.close()
edges_world.close()
