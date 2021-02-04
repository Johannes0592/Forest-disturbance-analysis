# computation of the breakpoints, monotonic trend and the metrics, which are finally used for the classification

library("strucchange")
library("bfast")
library("Kendall")
library("forecast")
setwd("F:/Studium_Trier/Masterarbeit/Datensaetze/tables")
valData <- read.csv("VItimeseries.csv", sep=";", header=TRUE,dec = ",")

monthlyNDVI <-cbind(as.vector(valData["NDVI180418"]),as.vector(valData["NDVI180505"]),as.vector(valData["NDVI180508"]),as.vector(valData["NDVI180702"]),as.vector(valData["NDVI180806"]),as.vector(valData["NDVI180912"]),as.vector(valData["NDVI190418"]),as.vector(valData["NDVI190515"]),as.vector(valData["NDVI190627"]),as.vector(valData["NDVI190724"]),as.vector(valData["NDVI190823"]),as.vector(valData["NDVI190915"]),as.vector(valData["NDVI200422"]),as.vector(valData["NDVI200507"]),as.vector(valData["NDVI200623"]),as.vector(valData["NDVI200731"]),as.vector(valData["NDVI200807"]),as.vector(valData["NDVI200921"]))

monthlyRE1 <-cbind(as.vector(valData["RE2180418"]),as.vector(valData["RE2180505"]),as.vector(valData["RE2180508"]),as.vector(valData["RE2180702"]),as.vector(valData["RE2180806"]),as.vector(valData["RE2180912"]),as.vector(valData["RE2190418"]),as.vector(valData["RE2190515"]),as.vector(valData["RE2190627"]),as.vector(valData["RE2190724"]),as.vector(valData["RE2190823"]),as.vector(valData["RE2190915"]),as.vector(valData["RE2200422"]),as.vector(valData["RE2200507"]),as.vector(valData["RE2200623"]),as.vector(valData["RE2200731"]),as.vector(valData["RE2200807"]),as.vector(valData["RE2200921"]))

monthlyRE2 <-cbind(as.vector(valData["RE3180418"]),as.vector(valData["NDVI180505"]),as.vector(valData["RE3180508"]),as.vector(valData["RE3180702"]),as.vector(valData["RE3180806"]),as.vector(valData["RE3180912"]),as.vector(valData["RE3190418"]),as.vector(valData["RE3190515"]),as.vector(valData["RE3190627"]),as.vector(valData["RE3190724"]),as.vector(valData["RE3190823"]),as.vector(valData["RE3190915"]),as.vector(valData["RE3200422"]),as.vector(valData["RE3200507"]),as.vector(valData["RE3200623"]),as.vector(valData["RE3200731"]),as.vector(valData["RE3200807"]),as.vector(valData["RE3200921"]))

monthlyNDMI <-cbind(as.vector(valData["NDMI180418"]),as.vector(valData["NDVI180505"]),as.vector(valData["NDMI180508"]),as.vector(valData["NDMI180702"]),as.vector(valData["NDMI180806"]),as.vector(valData["NDMI180912"]),as.vector(valData["NDMI190418"]),as.vector(valData["NDMI190515"]),as.vector(valData["NDMI190627"]),as.vector(valData["NDMI190724"]),as.vector(valData["NDMI190823"]),as.vector(valData["NDMI190915"]),as.vector(valData["NDMI200422"]),as.vector(valData["NDMI200507"]),as.vector(valData["NDMI200623"]),as.vector(valData["NDMI200731"]),as.vector(valData["NDMI200807"]),as.vector(valData["NDMI200921"]))

monthlyNDVI <- as.matrix(monthlyNDVI)
monthlyRE1 <- as.matrix(monthlyRE1)
monthlyRE2 <- as.matrix(monthlyRE2)
monthlyNDMI <- as.matrix(monthlyNDMI)

count <- 0
pb <- winProgressBar(title = "progress bar trend computation", min = 0,max = nrow(monthlyNDVI), width = 300)
trendsVI <- matrix(-1.1,ncol = 23, nrow = nrow(valData))
# compute trend component for each object
for(i in 1:nrow(valData)){
  #FID for later join in ArcGIS
  trendsVI[i,1] <- i-1
  
  NDVIts <- ts(monthlyNDVI[i,],frequency=6)
  RE1ts <- ts(monthlyRE1[i,],frequency=6)
  RE2ts <- ts(monthlyRE2[i,],frequency=6)
  NDMIts <- ts(monthlyNDMI[i,],frequency=6)
  
  
  # deseasonalization with stl for later use in breakpoint detection with strucchange
  bpNDVI <- NDVIts - stl(NDVIts,s.window = "periodic")$time.series[1:18]
  bpRE1 <- RE1ts - stl(RE1ts,s.window = "periodic")$time.series[1:18]
  bpRE2 <- RE2ts - stl(RE2ts,s.window = "periodic")$time.series[1:18]
  bpNDMI <- NDMIts - stl(NDMIts,s.window = "periodic")$time.series[1:18]
  
  # trend analysis with deseason data with  MannKendall 
  mkNDVI <- MannKendall(ts(bpNDVI,frequency=6))
  mkRE1 <- MannKendall(ts(bpRE1,frequency=6))
  mkRE2 <- MannKendall(ts(bpRE2,frequency=6))
  mkNDMI <- MannKendall(ts(bpNDMI,frequency=6))
  
  # assign significant trend and direction of trend
  if(mkNDVI$sl[1] < 0.05 & mkNDVI$tau[1] < 0){trendsVI[i,2]<-1}
  if(mkNDVI$sl[1] < 0.05 & mkNDVI$tau[1] > 0){trendsVI[i,2]<-2}
  
  if(mkRE1$sl[1] < 0.05 & mkRE1$tau[1] < 0){trendsVI[i,3]<-1}
  if(mkRE1$sl[1] < 0.05 & mkRE1$tau[1] > 0){trendsVI[i,3]<-2}
  
  if(mkRE2$sl[1] < 0.05 & mkRE2$tau[1] < 0){trendsVI[i,4]<-1}
  if(mkRE2$sl[1] < 0.05 & mkRE2$tau[1] > 0){trendsVI[i,4]<-2}
  
  if(mkNDMI$sl[1] < 0.05 & mkNDMI$tau[1] < 0){trendsVI[i,5]<-1}
  if(mkNDMI$sl[1] < 0.05 & mkNDMI$tau[1] > 0){trendsVI[i,5]<-2}
  
  
  # breakpoints with strucchange because bfast does not detect breaks in trend and seasonal component
  
  fsNDVI <- Fstats(ts(bpNDVI, frequency = 6)~1)
  fsRE1 <- Fstats(ts(bpRE1,frequency = 6)~1)
  fsRE2 <- Fstats(ts(bpRE2,frequency = 6)~1)
  fsNDMI <- Fstats(ts(bpNDMI,frequency = 6)~1)
  
  
  struNDVI <- breakpoints(fsNDVI,h=2,breaks=1)
  struRE1 <- breakpoints(fsRE1,h=2,breaks=1)
  struRE2 <- breakpoints(fsRE2,h=2,breaks=1)
  struNDMI <- breakpoints(fsNDMI,h=2,breaks=1)
  
  #magnitude of the breakpoint
  
  
  
  mag1 <- abs(as.numeric(NDVIts[struNDVI$breakpoints]-NDVIts[struNDVI$breakpoints+1]))
  mag2 <- abs(as.numeric(NDVIts[struNDVI$breakpoints]-NDVIts[struNDVI$breakpoints-1]))
  if(mag1<mag2){trendsVI[i,6] <- round(mag2,digits = 3)}
  else{trendsVI[i,6] <- round(mag1,digits = 3)}
  
  
  mag1 <- abs(as.numeric(RE1ts[struRE1$breakpoints]-RE1ts[struRE1$breakpoints+1]))
  mag2 <- abs(as.numeric(RE1ts[struRE1$breakpoints]-RE1ts[struRE1$breakpoints-1]))
  if(mag1<mag2){trendsVI[i,7] <- round(mag2,digits = 3)}
  else{trendsVI[i,7] <- round(mag1,digits = 3)}
  
  
  
  mag1 <- abs(as.numeric(RE2ts[struRE2$breakpoints]-RE2ts[struRE2$breakpoints+1]))
  mag2 <- abs(as.numeric(RE2ts[struRE2$breakpoints]-RE2ts[struRE2$breakpoints-1]))
  if(mag1<mag2){trendsVI[i,8] <- round(mag2,digits = 3)}
  else{trendsVI[i,8] <- round(mag1,digits = 3)}
  
  
  
  mag1 <- abs(as.numeric(NDMIts[struNDMI$breakpoints]-NDMIts[struNDMI$breakpoints+1]))
  mag2 <- abs(as.numeric(NDMIts[struNDMI$breakpoints]-NDMIts[struNDMI$breakpoints-1]))
  if(mag1<mag2){trendsVI[i,9] <- round(mag2,digits = 3)}
  else{trendsVI[i,9] <- round(mag1,digits = 3)}
  
  
  # pvalues for fstatistic
  
  if(sctest(fsNDVI, type="expF")$p < 0.05){trendsVI[i,10] <- sctest(fsNDVI, type="expF")$p}
  if(sctest(fsRE1, type="expF")$p < 0.05){trendsVI[i,11] <- sctest(fsRE1, type="expF")$p}
  if(sctest(fsRE2, type="expF")$p < 0.05){trendsVI[i,12] <- sctest(fsRE2, type="expF")$p}
  if(sctest(fsNDMI, type="expF")$p < 0.05){trendsVI[i,13] <- sctest(fsNDMI, type="expF")$p}
  
  # breakpoint date
  
  if(sctest(fsNDVI, type="expF")$p < 0.05) {trendsVI[i,14] <- struNDVI$breakpoints}
  if(sctest(fsRE1, type="expF")$p < 0.05){trendsVI[i,15] <- struRE1$breakpoints}
  if(sctest(fsRE2, type="expF")$p < 0.05){trendsVI[i,16] <- struRE2$breakpoints}
  if(sctest(fsNDMI, type="expF")$p < 0.05){trendsVI[i,17] <- struNDMI$breakpoints}
  
  # compute metrics magnitude post change, pre change, pre value, post value, pre rate post rate
  if(sctest(fsNDVI, type="expF")$p < 0.05) {
    trendsVI[i,18] <- as.numeric(NDVIts[struNDVI$breakpoints-1]) # preValue
    trendsVI[i,19] <- as.numeric(NDVIts[struNDVI$breakpoints+1]) # postValue
    trendsVI[i,20] <- as.numeric(NDVIts[1] - NDVIts[struNDVI$breakpoints]) # preChange
    trendsVI[i,21] <- as.numeric(NDVIts[struNDVI$breakpoints] - NDVIts[18]) # postChange
    trendsVI[i,22] <- as.numeric(lm(NDVIts[1:struNDVI$breakpoints]~seq(1:struNDVI$breakpoints))[[1]][2])  # preRate
    trendsVI[i,23] <- as.numeric(lm(NDVIts[(struNDVI$breakpoints+1):18]~seq((struNDVI$breakpoints+1):18))[[1]][2]) # postRate
    
  }
  
  
  
  count <- count+1
  setWinProgressBar(pb, i, title=paste( round(i/nrow(monthlyNDVI)*100, 0),"% trend computation finished"))
  
}
colnames(trendsVI) <- c("FID","trendNDVI","trendRE1","trendRE2","trendNDMI","magNDVI","magRE1","magRE2","magNDMI","pFNDVI","pFRE1","pFRE2","pFNDMI","bpNDVI","bpRE1","bpRE2","bpNDMI","preVal","postVal","preChange","postChange","preRate","postRate")
trendsVI <- as.data.frame(trendsVI)
write.csv2(trendsVI, "F:/Studium_Trier/Masterarbeit/Datensaetze/tables/test_breakpoints_significant.csv")
write.csv(trendsVI, "F:/Studium_Trier/Masterarbeit/Datensaetze/tables/trends.csv")

