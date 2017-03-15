args = commandArgs(trailingOnly=TRUE)

# Judge if the number of arguments is correct
if(length(args)<=1 || length(args)>=4) {
  cat("\n    Usage:\n       Rscript Enterotyping_v1.R <Data_input: spreadsheet> <Figure_output: PDF> <Number_of_clusters: integer, optional, better not>\n\n")
  quit()
  }

# User assign number of clusters
User_ncluster = FALSE
if(!is.na(args[3])) {
  User_ncluster = args[3]
}


# Path
path_input   = args[1]
path_output  = args[2]


# Load required packages
library(cluster)
library(clusterSim)
library(ade4)


# # Read data from file
data = read.table(path_input, header=T, sep="\t")
data$CAG      = NULL
data$Spearman = NULL
data$Gene     = NULL


# Example data sheet need to be seletcted, this row represents to reads can not be assign to known genus
# data = read.table(path_input, header=T, row.names=1, dec=".", sep="\t")
# data=data[-1,]


# Define function to calculate Jensen-Shannon Distance(JSD), clustering algorithm
dist.JSD <- function(inMatrix, pseudocount=0.000001, ...) {
  KLD <- function(x,y) sum(x *log(x/y))
  JSD <- function(x,y) sqrt(0.5 * KLD(x, (x+y)/2) + 0.5 * KLD(y, (x+y)/2))
  matrixColSize <- length(colnames(inMatrix))
  matrixRowSize <- length(rownames(inMatrix))
  colnames <- colnames(inMatrix)
  resultsMatrix <- matrix(0, matrixColSize, matrixColSize)
  
  inMatrix = apply(inMatrix,1:2,function(x) ifelse (x==0,pseudocount,x))
  
  for(i in 1:matrixColSize) {
    for(j in 1:matrixColSize) { 
      resultsMatrix[i,j] = JSD(as.vector(inMatrix[,i]),
                             as.vector(inMatrix[,j]))
    }
  }
  colnames -> colnames(resultsMatrix) -> rownames(resultsMatrix)
  as.dist(resultsMatrix) -> resultsMatrix
  attr(resultsMatrix, "method") <- "dist"
  return(resultsMatrix) 
}


# Apply 'data.dist' function to calculate the JSD
data.dist=dist.JSD(data)


# Partitioning Around Medoids(PAM) clustering algorithm, package 'cluster'
pam.clustering=function(x,k) {    # 'x' is a distance matrix and 'k' is the number of clusters
  require(cluster)
  cluster = as.vector(pam(as.dist(x), k, diss=TRUE)$clustering)    # 'pam(as.dist(x), k, diss=TRUE)' is the core of this function
  return(cluster)
}


# Optimal number of clusters and cluster (original code of this section has been revised)
require(clusterSim)

data.cluster    = 0
CHI             = 0    # Calinski-Harabasz (CH) Index, package 'clusterSim'
optimal_k       = 3    # Defualt k is 3
maxNum_clusters = 20   # Maximun of trial
# Start trying the best 'data.cluster'
for (k in 1:maxNum_clusters) {
  if (k==1) {
    CHI=0
  } else {
    data.cluster_temp=pam.clustering(data.dist, k)    # Apply 'pam.clustering' function to cluster the abundance profiles
    CHI_tmp = index.G1(t(data),data.cluster_temp,  d = data.dist, centrotypes = "medoids")    # Calculate the Calinski-Harabasz (CH) Index
    if (CHI_tmp>CHI) {
      CHI          = CHI_tmp
      data.cluster = data.cluster_temp
      optimal_k    = k
    }
  }
}

# In case that user doesn't need CH index optimization
if (User_ncluster) {
  data.cluster=pam.clustering(data.dist, optimal_k)
}


# Cluster validation, 'silhouette' from package 'cluster'
obs.silhouette = mean(silhouette(data.cluster, data.dist)[,3])


# Graphical interpretation, PCoA(Principal coordinate analysis)
require(ade4)
obs.pcoa=dudi.pco(data.dist, scannf=F, nf=3)    # PCoA calculation

# Out the result as PDF file
pdf(path_output)
s.class(obs.pcoa$li, fac=as.factor(data.cluster), grid=F, col=c(1,2,3,4,5,6,7,8,9,10,11,12,12,14,15,16,17,18,19,20))    # Drawing the figure
dev.off()






