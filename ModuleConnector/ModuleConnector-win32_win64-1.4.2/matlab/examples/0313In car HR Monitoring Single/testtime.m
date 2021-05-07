a = 123456;
plot(1:6,[1,3,2,5,4,3]);


textstr=sprintf('%d:%d:%d',floor(a/10000),floor(mod(a,10000)/100),mod(a,100));
text(1,1.2,{textstr},'FontSize',12,'FontWeight','bold','color','red');