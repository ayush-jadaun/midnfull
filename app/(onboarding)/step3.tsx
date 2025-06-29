import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import LottieLoader from "../../components/LottieLoader";
import { router } from "expo-router";

export default function OnboardingStep3() {
  return (
    <View style={styles.container}>
      <LottieLoader source={require("../../assets/lottie/onboarding3.json")} />
      <Text style={styles.title}>Mindfulness Tools</Text>
      <Text style={styles.text}>
        Explore a library of guided meditations, breathing exercises, and gentle
        reminders. Let your phone be a source of calm, not stress.
      </Text>
      <Button
        title="Get Started"
        color="#6C63FF"
        onPress={() => router.replace("/")}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#D6CDEA", // Lavender
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#6C63FF",
    marginBottom: 20,
  },
  text: {
    fontSize: 18,
    color: "#2D3A4A",
    textAlign: "center",
    marginBottom: 40,
  },
});
